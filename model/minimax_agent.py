"""Agente Minimax recursivo con contador de nodos.

Solo logica de busqueda, sin Flask ni HTML. Usa backtracking
(make/undo) y la funcion evaluate() del bloque 1.
"""

from model.evaluation import AI_PLAYER, HUMAN_PLAYER, evaluate
from model.game_model import BOARD_SIZE, EMPTY, TicTacToeModel


def best_move(juego):
    """Elige la mejor jugada para la IA (O).

    Args:
        juego: Instancia de TicTacToeModel con el estado actual.

    Returns:
        Tupla (movimiento, nodos) donde movimiento es (fila, col)
        o None si no hay jugadas, y nodos es la cantidad de
        estados explorados.
    """
    nodos = [0]
    mejor_valor = float("-inf")
    mejor_jugada = None

    for move in juego.get_available_moves():
        juego.make_move(move, AI_PLAYER)
        valor = _minimax(juego.board, False, nodos)
        juego.undo_move(move)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_jugada = move

    return mejor_jugada, nodos[0]


def _minimax(board, es_maximo, nodos):
    """Recorre el arbol y devuelve la mejor puntuacion posible.

    Args:
        board: Matriz de 3x3 que se modifica y revierte in situ.
        es_maximo: True si toca a la IA (maximiza), False si al
            humano (minimiza).
        nodos: Lista de un elemento usada como contador mutable.

    Returns:
        Puntuacion +10, -10, 0 segun evaluate().
    """
    nodos[0] += 1

    puntos = evaluate(board)
    if puntos is not None:
        return puntos

    if es_maximo:
        mejor = float("-inf")
        for row, col in _vacias(board):
            board[row][col] = AI_PLAYER
            mejor = max(mejor, _minimax(board, False, nodos))
            board[row][col] = EMPTY
        return mejor

    peor = float("inf")
    for row, col in _vacias(board):
        board[row][col] = HUMAN_PLAYER
        peor = min(peor, _minimax(board, True, nodos))
        board[row][col] = EMPTY
    return peor


def _vacias(board):
    """Devuelve las casillas vacias en orden fila por fila.

    Args:
        board: Matriz de 3x3.

    Returns:
        Lista de tuplas (fila, columna).
    """
    libres = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                libres.append((row, col))
    return libres


