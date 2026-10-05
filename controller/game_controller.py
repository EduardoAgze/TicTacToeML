"""Controlador: enlaza el modelo con las vistas."""
from flask import render_template, request, redirect, url_for # type: ignore
from model.game_model import (
    TicTacToeModel,
    PLAYER_X,
    PLAYER_O,
    RESULT_WIN,
    RESULT_DRAW,
    RESULT_INVALID,
    RESULT_CONTINUE,
)

# Estado de la partida (una sola por ahora).
juego = TicTacToeModel()
mensaje = ""


def get_estado():
    """Devuelve (ganador, terminado)."""
    if juego.check_winner(PLAYER_X):
        return PLAYER_X, True
    if juego.check_winner(PLAYER_O):
        return PLAYER_O, True
    if juego.is_draw():
        return None, True
    return None, False


def index():
    """GET / : muestra el tablero."""
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
    """POST /move : aplica una jugada del formulario."""
    global mensaje
    try:
        row = int(request.form["row"])
        col = int(request.form["col"])
    except (KeyError, ValueError):
        mensaje = "Movimiento inválido."
        return redirect(url_for("index"))

    resultado = juego.play_turn((row, col))

    if resultado == RESULT_WIN:
        mensaje = f"¡Jugador {juego.current_player} gana!"
    elif resultado == RESULT_DRAW:
        mensaje = "Empate."
    elif resultado == RESULT_INVALID:
        mensaje = "Casilla ocupada o fuera de rango."
    elif resultado == RESULT_CONTINUE:
        mensaje = ""

    return redirect(url_for("index"))


def reset():
    """POST /reset : reinicia la partida."""
    global mensaje
    juego.reset()
    mensaje = ""
    return redirect(url_for("index"))
