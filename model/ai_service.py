"""Servicio de IA: elige jugada (Minimax o ML) y mide metricas.

Aisla toda la logica de IA del controlador: carga del modelo,
inferencia, fallback a Minimax y contadores educativos.
"""

import time
from dataclasses import dataclass
from typing import Optional, Tuple

from model.minimax_agent import best_move

MODEL_PATH = "model/tictactoe_dt.joblib"

DIFICULTADES = ("facil", "medio", "dificil")
PROFUNDIDAD_MINIMAX = {"facil": 1, "medio": 2, "dificil": None}

_MODEL = None
_MODEL_CARGADO = False




def _modelo():
    """Carga el modelo ML una sola vez (lazy, tolerante a fallos).

    Returns:
        Clasificador o None si no esta disponible.
    """
    global _MODEL, _MODEL_CARGADO
    if _MODEL_CARGADO:
        return _MODEL
    try:
        import joblib

        _MODEL = joblib.load(MODEL_PATH)
    except (ImportError, OSError, ValueError):
        _MODEL = None
    _MODEL_CARGADO = True
    return _MODEL


def choose_move(juego, modo, dificultad="dificil"):
    """Elige la jugada de la IA segun el modo.

    Args:
        juego: Instancia de TicTacToeModel con el estado actual.
        modo: 'hvai' (Minimax) o 'hvml' (Machine Learning).
        dificultad: 'facil', 'medio' o 'dificil'. Solo afecta a
            Minimax; el ML siempre usa el mismo modelo.

    Returns:
        MoveResult con la jugada y sus metricas.
    """
    if modo == "hvai":
        return _elige_minimax(juego, dificultad)
    if modo == "hvml":
        return _elige_ml(juego)
    return MoveResult()


def _elige_minimax(juego, dificultad="dificil"):
    """Decide con Minimax y mide nodos y tiempo.

    Args:
        juego: Instancia de TicTacToeModel con el estado actual.
        dificultad: Nivel que determina la profundidad de busqueda.
    """
    profundidad = PROFUNDIDAD_MINIMAX.get(dificultad)
    inicio = time.perf_counter()
    jugada, total = best_move(juego, max_depth=profundidad)
    tiempo = (time.perf_counter() - inicio) * 1000.0
    return MoveResult(
        move=jugada,
        nodos=total,
        tiempo_ms=tiempo,
        origen="minimax",
    )


def _elige_ml(juego):
    """Decide con el arbol ML y cae en Minimax si es ilegal."""
    from model.ml_agent import decode_label, encode_board

    clf = _modelo()
    estado = encode_board(juego.board)
    inicio = time.perf_counter()
    jugada = None
    if clf is not None:
        try:
            label = int(clf.predict([estado])[0])
            candidata = decode_label(label)
            if juego.is_valid_move(candidata):
                jugada = candidata
        except (ValueError, IndexError):
            jugada = None
    if jugada is None:
        resultante = _elige_minimax(juego)
        resultante.nodos = -1
        resultante.origen = "fallback"
        return resultante
    tiempo = (time.perf_counter() - inicio) * 1000.0
    return MoveResult(
        move=jugada,
        nodos=0,
        tiempo_ms=tiempo,
        origen="ml",
    )

@dataclass
class MoveResult:
    """Resultado de una decision de la IA.

    Attributes:
        move: Tupla (fila, columna) o None si no hay jugada.
        nodos: Nodos explorados (-1 si hubo fallback, 0 si ML).
        tiempo_ms: Milisegundos de la decision.
        origen: 'minimax', 'ml' o 'fallback'.
    """

    move: Optional[Tuple[int, int]] = None
    nodos: int = 0
    tiempo_ms: float = 0.0
    origen: str = ""
