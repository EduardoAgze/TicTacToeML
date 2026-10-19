"""Estado de una partida en curso y orquestacion de turnos.

Agrupa tablero, modo y metricas en un objeto, en vez de usar
variables globales sueltas en el controlador.
"""

from model.ai_service import MoveResult, choose_move
from model.game_model import (
    RESULT_CONTINUE,
    RESULT_DRAW,
    RESULT_INVALID,
    RESULT_WIN,
    TicTacToeModel,
)

MODOS = ("hvh", "hvai", "hvml")


def _mensaje(resultado, jugador):
    """Devuelve el texto de estado segun el resultado del turno.

    Args:
        resultado: Uno de 'win', 'draw', 'invalid', 'continue'.
        jugador: Jugador que acaba de mover ('X' u 'O').

    Returns:
        Mensaje para mostrar en la vista.
    """
    if resultado == RESULT_WIN:
        return "¡Jugador {} gana!".format(jugador)
    if resultado == RESULT_DRAW:
        return "Empate."
    if resultado == RESULT_INVALID:
        return "Casilla ocupada o fuera de rango."
    return ""


class GameSession:
    """Reune el tablero, el modo y las metricas de la ultima IA."""

    def __init__(self):
        """Crea una sesion nueva en modo Humano vs IA Minimax."""
        self.juego = TicTacToeModel()
        self.modo = "hvai"
        self.mensaje = ""
        self.metricas = MoveResult()
        self.reset()

    def reset(self):
        """Reinicia el tablero y las metricas conservando el modo."""
        self.juego.reset()
        self.mensaje = ""
        self.metricas = MoveResult()

    def set_modo(self, modo):
        """Cambia el modo de juego y reinicia la partida.

        Args:
            modo: 'hvh', 'hvai' o 'hvml'; otro valor cae en 'hvai'.
        """
        self.modo = modo if modo in MODOS else "hvai"
        self.reset()

    def marcar_invalido(self):
        """Registra que llego un movimiento con formato invalido."""
        self.mensaje = "Movimiento invalido."

    def play(self, move):
        """Aplica el turno humano y responde con la IA si toca.

        Args:
            move: Tupla (fila, columna) jugada por la persona.

        Returns:
            El resultado de `play_turn`: win, draw, invalid o continue.
        """
        resultado = self.juego.play_turn(move)
        self.mensaje = _mensaje(resultado, self.juego.current_player)
        if resultado == RESULT_CONTINUE:
            self._juega_ia()
        return resultado

    def _juega_ia(self):
        """Delega la decision en el servicio de IA y guarda metricas."""
        if self.modo == "hvh":
            return
        if self.juego.is_game_over():
            return
        resultado = choose_move(self.juego, self.modo)
        self.metricas = resultado
        if resultado.move is None:
            return
        self.mensaje = _mensaje(
            self.juego.play_turn(resultado.move),
            self.juego.current_player,
        )

    @property
    def ganador(self):
        """Devuelve 'X', 'O' o None."""
        return self.juego.winner()

    @property
    def terminado(self):
        """Indica si la partida termino."""
        return self.juego.is_game_over()

    @property
    def nodos(self):
        """Nodos explorados por la ultima IA."""
        return self.metricas.nodos

    @property
    def tiempo_ms(self):
        """Milisegundos de la ultima decision de la IA."""
        return self.metricas.tiempo_ms

    @property
    def ruta(self):
        """Ids de nodo del arbol ML usados en la ultima decision."""
        return self.metricas.ruta
