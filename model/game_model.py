"""Modelo y reglas del juego Tres en Raya."""

BOARD_SIZE = 3
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

RESULT_INVALID = 'invalid'
RESULT_WIN = 'win'
RESULT_DRAW = 'draw'
RESULT_CONTINUE = 'continue'


class TicTacToeModel:
    """Gestiona el estado y las reglas del juego."""

    def __init__(self):
        """Inicializa una partida nueva."""
        self.reset()

    def reset(self):
        """Vacía el tablero y asigna el turno a X."""
        self.board = []
        for row in range(BOARD_SIZE):
            fila_nueva = []
            for col in range(BOARD_SIZE):
                fila_nueva.append(EMPTY)
            self.board.append(fila_nueva)
        self.current_player = PLAYER_X

    def is_valid_move(self, move):
        """Comprueba que la posición esté dentro del tablero y vacía."""
        row, col = move
        fila_existe = 0 <= row < BOARD_SIZE
        columna_existe = 0 <= col < BOARD_SIZE

        if not fila_existe or not columna_existe:
            return False

        casilla_libre = self.board[row][col] == EMPTY
        return casilla_libre

    def get_available_moves(self):
        """Devuelve las posiciones vacías como tuplas (fila, columna)."""
        movimientos = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == EMPTY:
                    movimientos.append((row, col))

        return movimientos

    def get_cell(self, row, col):
        """Devuelve el contenido de una casilla."""
        return self.board[row][col]

    def _get_all_lines(self):
        """Devuelve las filas, columnas y diagonales del tablero."""
        lines = []

        for row in range(BOARD_SIZE):
            lines.append(self.board[row])

        for col in range(BOARD_SIZE):
            columna = []

            for row in range(BOARD_SIZE):
                columna.append(self.board[row][col])

            lines.append(columna)

        diagonal_principal = []

        for i in range(BOARD_SIZE):
            diagonal_principal.append(self.board[i][i])

        lines.append(diagonal_principal)

        diagonal_secundaria = []

        for i in range(BOARD_SIZE):
            columna_invertida = BOARD_SIZE - 1 - i
            diagonal_secundaria.append(self.board[i][columna_invertida])

        lines.append(diagonal_secundaria)

        return lines

    def check_winner(self, player):
        """Comprueba si el jugador completó una línea."""
        todas_las_lineas = self._get_all_lines()

        for linea in todas_las_lineas:
            linea_completa = True

            for casilla in linea:
                if casilla != player:
                    linea_completa = False

            if linea_completa:
                return True

        return False

    def is_draw(self):
        """Comprueba si el tablero está lleno y no hay ganador."""
        movimientos_libres = self.get_available_moves()
        tablero_lleno = len(movimientos_libres) == 0

        x_gano = self.check_winner(PLAYER_X)
        o_gano = self.check_winner(PLAYER_O)
        alguien_gano = x_gano or o_gano

        return tablero_lleno and not alguien_gano

    def is_game_over(self):
        """Comprueba si la partida terminó."""
        x_gano = self.check_winner(PLAYER_X)
        o_gano = self.check_winner(PLAYER_O)
        hay_empate = self.is_draw()

        return x_gano or o_gano or hay_empate

    def make_move(self, move, player):
        """Coloca la ficha del jugador en la posición indicada."""
        row, col = move
        self.board[row][col] = player

    def undo_move(self, move):
        """Vacía la posición indicada."""
        row, col = move
        self.board[row][col] = EMPTY

    def play_turn(self, move):
        """Ejecuta un turno y devuelve su resultado."""
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
        """Alterna entre X y O."""
        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X