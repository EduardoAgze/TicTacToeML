"""Modelo y reglas del juego Tres en Raya.
"""

BOARD_SIZE = 3
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

RESULT_INVALID = 'invalid'
RESULT_WIN = 'win'
RESULT_DRAW = 'draw'
RESULT_CONTINUE = 'continue'


class TicTacToeModel:
    """Gestiona el estado y las reglas del juego.

    Attributes:
        board: Matriz de 3x3 con 'X', 'O' o ' '.
        current_player: Jugador con el turno ('X' o 'O').
    """

    def __init__(self):
        """Inicializa una partida nueva con el tablero vacio."""
        self.reset()

    def reset(self):
        """Vacia el tablero y asigna el turno a X."""
        self.board = []
        for _ in range(BOARD_SIZE):
            fila_nueva = [EMPTY] * BOARD_SIZE
            self.board.append(fila_nueva)
        self.current_player = PLAYER_X

    def is_valid_move(self, move):
        """Comprueba que la posicion este dentro del tablero y vacia.

        Args:
            move: Tupla (fila, columna) con la posicion a jugar.

        Returns:
            True si la casilla existe y esta vacia, False si no.
        """
        row, col = move
        fila_existe = 0 <= row < BOARD_SIZE
        columna_existe = 0 <= col < BOARD_SIZE

        if not fila_existe or not columna_existe:
            return False

        return self.board[row][col] == EMPTY

    def get_available_moves(self):
        """Devuelve las posiciones vacias del tablero.

        Returns:
            Lista de tuplas (fila, columna) con las casillas libres.
        """
        movimientos = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == EMPTY:
                    movimientos.append((row, col))
        return movimientos

    def get_cell(self, row, col):
        """Devuelve el contenido de una casilla.

        Args:
            row: Indice de fila (0 a 2).
            col: Indice de columna (0 a 2).

        Returns:
            'X', 'O' o ' ' segun el contenido de la casilla.
        """
        return self.board[row][col]

    def _get_all_lines(self):
        """Devuelve las filas, columnas y diagonales del tablero.

        Returns:
            Lista con las 8 lineas posibles (3 filas, 3 columnas
            y 2 diagonales).
        """
        lines = []

        for row in range(BOARD_SIZE):
            lines.append(self.board[row])

        for col in range(BOARD_SIZE):
            columna = [self.board[row][col] for row in range(BOARD_SIZE)]
            lines.append(columna)

        diagonal_principal = [self.board[i][i] for i in range(BOARD_SIZE)]
        lines.append(diagonal_principal)

        diagonal_secundaria = [
            self.board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)
        ]
        lines.append(diagonal_secundaria)

        return lines

    def check_winner(self, player):
        """Comprueba si el jugador completo alguna linea.

        Args:
            player: 'X' o 'O'.

        Returns:
            True si el jugador gano, False si no.
        """
        for linea in self._get_all_lines():
            if all(casilla == player for casilla in linea):
                return True
        return False

    def is_draw(self):
        """Comprueba si el tablero esta lleno y no hay ganador.

        Returns:
            True si hay empate, False si no.
        """
        tablero_lleno = len(self.get_available_moves()) == 0
        alguien_gano = (
            self.check_winner(PLAYER_X) or self.check_winner(PLAYER_O)
        )
        return tablero_lleno and not alguien_gano

    def is_game_over(self):
        """Comprueba si la partida termino por victoria o empate.

        Returns:
            True si alguien gano o hay empate, False si no.
        """
        return (
            self.check_winner(PLAYER_X)
            or self.check_winner(PLAYER_O)
            or self.is_draw()
        )

    def make_move(self, move, player):
        """Coloca la ficha del jugador en la posicion indicada.

        Args:
            move: Tupla (fila, columna).
            player: 'X' o 'O'.
        """
        row, col = move
        self.board[row][col] = player

    def undo_move(self, move):
        """Vacia la posicion indicada (para IA / busqueda).

        Args:
            move: Tupla (fila, columna).
        """
        row, col = move
        self.board[row][col] = EMPTY

    def play_turn(self, move):
        """Ejecuta un turno con el jugador actual.

        Args:
            move: Tupla (fila, columna) con la posicion a jugar.

        Returns:
            Uno de: 'invalid', 'win', 'draw' o 'continue'.
        """
        if not self.is_valid_move(move):
            return RESULT_INVALID

        self.make_move(move, self.current_player)

        if self.check_winner(self.current_player):
            return RESULT_WIN

        if self.is_draw():
            return RESULT_DRAW

        self._switch_player()
        return RESULT_CONTINUE

    def _switch_player(self):
        """Alterna el turno entre X y O."""
        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

