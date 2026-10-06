from flask import redirect, render_template, request, url_for

from model.game_model import (
    PLAYER_O,
    PLAYER_X,
    RESULT_CONTINUE,
    RESULT_DRAW,
    RESULT_INVALID,
    RESULT_WIN,
    TicTacToeModel,
)

juego = TicTacToeModel()
mensaje = ""


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
    )


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

    if resultado == RESULT_WIN:
        mensaje = "¡Jugador {} gana!".format(juego.current_player)
    elif resultado == RESULT_DRAW:
        mensaje = "Empate."
    elif resultado == RESULT_INVALID:
        mensaje = "Casilla ocupada o fuera de rango."
    elif resultado == RESULT_CONTINUE:
        mensaje = ""

    return redirect(url_for("index"))


def reset():
    """Reinicia la partida (POST /reset).

    Returns:
        Redireccion a `index` con el tablero vacio.
    """
    global mensaje
    juego.reset()
    mensaje = ""
    return redirect(url_for("index"))
