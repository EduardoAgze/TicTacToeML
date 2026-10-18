"""Controlador que enlaza el modelo con las vistas."""

import time

from flask import redirect, render_template, request, url_for

from model.evaluation import AI_PLAYER
from model.game_model import (
    PLAYER_O,
    PLAYER_X,
    RESULT_CONTINUE,
    RESULT_DRAW,
    RESULT_INVALID,
    RESULT_WIN,
    TicTacToeModel,
)
from model.minimax_agent import best_move

juego = TicTacToeModel()
mensaje = ""
modo = "hvai"
ultimo_nodos = 0
ultimo_tiempo_ms = 0.0
ultima_ruta = []
_ml_model = None
_tree_cache = None
MODOS = ("hvh", "hvai", "hvml")
MODEL_PATH = "model/tictactoe_dt.joblib"
TREE_MAX_DEPTH = 4


def get_estado():
    """Devuelve el ganador y si la partida termino.

    Returns:
        Tupla (ganador, terminado) donde ganador es 'X', 'O' o None.
    """
    if juego.check_winner(PLAYER_X):
        return PLAYER_X, True
    if juego.check_winner(PLAYER_O):
        return PLAYER_O, True
    if juego.is_draw():
        return None, True
    return None, False


def index():
    """Muestra el tablero actual (GET /).

    Returns:
        Plantilla `index.html` con tablero, turno y mensaje.
    """
    ganador, terminado = get_estado()
    return render_template(
        "index.html",
        board=juego.board,
        turno=juego.current_player,
        ganador=ganador,
        terminado=terminado,
        mensaje=mensaje,
        modo=modo,
        nodos=ultimo_nodos,
        tiempo_ms=ultimo_tiempo_ms,
        tree=_get_tree_json() if modo == "hvml" else None,
        ruta=ultima_ruta if modo == "hvml" else [],
    )


def _actualiza_mensaje(resultado):
    """Actualiza el mensaje global segun el resultado.

    Args:
        resultado: Uno de 'win', 'draw', 'continue', 'invalid'.
    """
    global mensaje
    if resultado == RESULT_WIN:
        mensaje = "¡Jugador {} gana!".format(juego.current_player)
    elif resultado == RESULT_DRAW:
        mensaje = "Empate."
    elif resultado == RESULT_INVALID:
        mensaje = "Casilla ocupada o fuera de rango."
    elif resultado == RESULT_CONTINUE:
        mensaje = ""


def _juega_ia():
    """Hace jugar a la IA Minimax si toca su turno en modo HvAI."""
    global ultimo_nodos, ultimo_tiempo_ms
    if modo != "hvai":
        return
    if get_estado()[1]:
        return
    if juego.current_player != AI_PLAYER:
        return
    inicio = time.perf_counter()
    jugada, total = best_move(juego)
    ultimo_tiempo_ms = (time.perf_counter() - inicio) * 1000.0
    ultimo_nodos = total
    if jugada is None:
        return
    _actualiza_mensaje(juego.play_turn(jugada))


def _carga_modelo_ml():
    """Carga el arbol ML una sola vez (lazy, sin romper sin sklearn).

    Returns:
        Clasificador o None si no existe el archivo.
    """
    global _ml_model
    if _ml_model is not None:
        return _ml_model
    try:
        import joblib
    except ImportError:
        return None
    try:
        _ml_model = joblib.load(MODEL_PATH)
    except (OSError, ValueError):
        return None
    return _ml_model


def _get_tree_json():
    """Devuelve el arbol exportado a JSON (cacheado).

    Returns:
        Diccionario del arbol o None si no hay modelo.
    """
    global _tree_cache
    if _tree_cache is not None:
        return _tree_cache
    clf = _carga_modelo_ml()
    if clf is None:
        return None
    from model.tree_export import export_tree_json

    _tree_cache = export_tree_json(clf, max_depth=TREE_MAX_DEPTH)
    return _tree_cache


def _juega_ml():
    """Hace jugar a la IA ML si toca su turno en modo HvML."""
    global ultimo_nodos, ultimo_tiempo_ms, ultima_ruta
    if modo != "hvml":
        return
    if get_estado()[1]:
        return
    if juego.current_player != AI_PLAYER:
        return
    from model.ml_agent import decode_label, encode_board
    from model.tree_export import active_path

    clf = _carga_modelo_ml()
    estado = encode_board(juego.board)
    inicio = time.perf_counter()
    jugada = None
    if clf is not None:
        try:
            label = int(clf.predict([estado])[0])
            ultima_ruta = active_path(clf, estado)
            cand = decode_label(label)
            if juego.is_valid_move(cand):
                jugada = cand
        except (ValueError, IndexError):
            jugada = None
            ultima_ruta = []
    if jugada is None:
        jugada, _ = best_move(juego)
        ultimo_nodos = -1
    else:
        ultimo_nodos = 0
    ultimo_tiempo_ms = (time.perf_counter() - inicio) * 1000.0
    if jugada is None:
        return
    _actualiza_mensaje(juego.play_turn(jugada))


def move():
    """Aplica una jugada enviada por formulario (POST /move).

    Returns:
        Redireccion a `index` con el mensaje actualizado.
    """
    global mensaje
    try:
        row = int(request.form["row"])
        col = int(request.form["col"])
    except (KeyError, ValueError):
        mensaje = "Movimiento invalido."
        return redirect(url_for("index"))

    resultado = juego.play_turn((row, col))

    _actualiza_mensaje(resultado)
    if resultado == RESULT_CONTINUE:
        _juega_ia()
        _juega_ml()

    return redirect(url_for("index"))


def set_mode():
    """Cambia el modo de juego y reinicia (POST /mode).

    Returns:
        Redireccion a `index` con el tablero vacio.
    """
    global mensaje, modo, ultimo_nodos, ultimo_tiempo_ms, ultima_ruta
    elegido = request.form.get("modo", "hvai")
    modo = elegido if elegido in MODOS else "hvai"
    juego.reset()
    mensaje = ""
    ultimo_nodos = 0
    ultimo_tiempo_ms = 0.0
    ultima_ruta = []
    return redirect(url_for("index"))


def reset():
    """Reinicia la partida (POST /reset).

    Returns:
        Redireccion a `index` con el tablero vacio.
    """
    global mensaje, ultimo_nodos, ultimo_tiempo_ms, ultima_ruta
    juego.reset()
    mensaje = ""
    ultimo_nodos = 0
    ultimo_tiempo_ms = 0.0
    ultima_ruta = []
    return redirect(url_for("index"))
