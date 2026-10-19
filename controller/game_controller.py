"""Controlador HTTP: traduce peticiones y delega en GameSession.

No contiene reglas del juego ni logica de IA; eso vive en el
modelo (`game_model`) y en el servicio (`ai_service`).
"""

from flask import redirect, render_template, request, url_for

from model.ai_service import tree_json
from model.session import GameSession

session = GameSession()


def index():
    """Muestra el tablero actual (GET /).

    Returns:
        Plantilla `index.html` con tablero, turno y metricas.
    """
    return render_template(
        "index.html",
        board=session.juego.board,
        turno=session.juego.current_player,
        ganador=session.ganador,
        terminado=session.terminado,
        mensaje=session.mensaje,
        modo=session.modo,
        nodos=session.nodos,
        tiempo_ms=session.tiempo_ms,
        tree=tree_json() if session.modo == "hvml" else None,
        ruta=session.ruta if session.modo == "hvml" else [],
    )


def move():
    """Aplica una jugada enviada por formulario (POST /move).

    Returns:
        Redireccion a `index` con la partida actualizada.
    """
    try:
        row = int(request.form["row"])
        col = int(request.form["col"])
    except (KeyError, ValueError):
        session.marcar_invalido()
        return redirect(url_for("index"))

    session.play((row, col))
    return redirect(url_for("index"))


def set_mode():
    """Cambia el modo de juego y reinicia (POST /mode).

    Returns:
        Redireccion a `index` con el tablero vacio.
    """
    session.set_modo(request.form.get("modo", "hvai"))
    return redirect(url_for("index"))


def reset():
    """Reinicia la partida (POST /reset).

    Returns:
        Redireccion a `index` con el tablero vacio.
    """
    session.reset()
    return redirect(url_for("index"))
