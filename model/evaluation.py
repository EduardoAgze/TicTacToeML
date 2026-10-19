"""Funcion de evaluacion heuristica para estados terminales.

Convencion: Humano = X, IA = O. La puntuacion es desde la vista de la IA.
"""

from model.game_model import EMPTY, PLAYER_O, PLAYER_X

AI_PLAYER = PLAYER_O
HUMAN_PLAYER = PLAYER_X

SCORE_WIN = 10
SCORE_LOSS = -10
SCORE_DRAW = 0

# Las 8 lineas ganadoras como coordenadas (fila, columna).
WINNING_LINES = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
)


def evaluate(board):
    """Evalua un tablero y devuelve su puntuacion.

    Args:
        board: Matriz de 3x3 con 'X', 'O' o ' '.

    Returns:
        +10 si gana la IA (O), -10 si gana el humano (X),
        0 si hay empate, None si la partida sigue abierta.
    """
    if _wins(board, AI_PLAYER):
        return SCORE_WIN
    if _wins(board, HUMAN_PLAYER):
        return SCORE_LOSS
    if _is_full(board):
        return SCORE_DRAW
    return None


def _wins(board, player):
    """Comprueba si el jugador completo alguna de las 8 lineas.

    Args:
        board: Matriz de 3x3.
        player: 'X' o 'O'.

    Returns:
        True si el jugador gano, False si no.
    """
    return any(
        all(board[row][col] == player for row, col in line)
        for line in WINNING_LINES
    )


def _is_full(board):
    """Comprueba si no quedan casillas vacias.

    Args:
        board: Matriz de 3x3.

    Returns:
        True si el tablero esta lleno, False si no.
    """
    for row in board:
        if EMPTY in row:
            return False
    return True
