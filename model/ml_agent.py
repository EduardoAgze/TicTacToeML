"""Herramienta de simulacion para datos sinteticos (Semana 3).

Genera partidas Minimax (O) vs aleatorio (X) y guarda cada estado
previo a mover O junto a la jugada optima. Sin sklearn aqui.
"""

import csv
import os
import random

from model.game_model import PLAYER_O, PLAYER_X, TicTacToeModel
from model.minimax_agent import best_move

CODIGO = {" ": 0, "X": 1, "O": 2}


def encode_board(board):
    """Codifica el tablero 3x3 en 9 enteros fila por fila.

    Args:
        board: Matriz de 3x3 con ' ', 'X' u 'O'.

    Returns:
        Lista de 9 enteros (0= vacio, 1=X, 2=O).
    """
    return [CODIGO[board[r][c]] for r in range(3) for c in range(3)]


def decode_label(label):
    """Convierte etiqueta 0-8 en (fila, columna).

    Args:
        label: Entero de 0 a 8.

    Returns:
        Tupla (fila, columna).
    """
    return divmod(int(label), 3)


def generate_dataset(n_games=300, csv_path="data/dataset.csv", seed=42):
    """Simula partidas y guarda estados de O con su jugada optima.

    Args:
        n_games: Cantidad de partidas a simular.
        csv_path: Ruta del CSV a escribir.
        seed: Semilla para reproducibilidad.

    Returns:
        Cantidad de filas escritas (un estado por turno de O).
    """
    random.seed(seed)
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)

    filas = 0
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["c0", "c1", "c2", "c3", "c4",
                         "c5", "c6", "c7", "c8", "label"])
        for _ in range(n_games):
            juego = TicTacToeModel()
            while not juego.is_game_over():
                if juego.current_player == PLAYER_X:
                    move = random.choice(juego.get_available_moves())
                    juego.play_turn(move)
                else:
                    estado = encode_board(juego.board)
                    mejor, _ = best_move(juego)
                    if mejor is None:
                        break
                    label = mejor[0] * 3 + mejor[1]
                    writer.writerow(estado + [label])
                    filas += 1
                    juego.play_turn(mejor)
                    if juego.check_winner(PLAYER_O):
                        break
    return filas


if __name__ == "__main__":
    total = generate_dataset()
    print("Filas:", total)
