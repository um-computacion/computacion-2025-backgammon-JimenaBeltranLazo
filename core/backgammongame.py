from core.board import Board
from core.dice import DiceGameLogic
from core.player import Player


class TurnManager: # Solo maneja el turno actual
    def __init__(self, jugador_blanco: Player, jugador_negro: Player):
        self.jugador_blanco = jugador_blanco
        self.jugador_negro = jugador_negro
        self.__jugador_actual__ = None
        self.__tiradas_iniciales__ = {} # Guarda tiradas iniciales de cada jugador
        self.__turno_determinado__ = False

    def determinar_primer_turno(self, dado):
        if not self.__turno_determinado__: # Si el turno no se ha sido determinado
            if "Blanco" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Blanco"] = dado
            elif "Negro" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Negro"] = dado
                self.__turno_determinado__ = True
                if self.__tiradas_iniciales__["Blanco"] > self.__tiradas_iniciales__["Negro"]: # Compara el valor de los dados de ambos jugadores
                    self.__jugador_actual__ = self.jugador_blanco
                elif self.__tiradas_iniciales__["Negro"] > self.__tiradas_iniciales__["Blanco"]:
                    self.__jugador_actual__ = self.jugador_negro

    def cambiar_turno(self):
        self.__jugador_actual__ = (
            self.jugador_negro if self.__jugador_actual__ == self.jugador_blanco # Cambia a jugador negro
            else self.jugador_blanco
        )

    def obtener_jugador_actual(self) -> Player:
        return self.__jugador_actual__


class MoveManager: # Solo valida y ejecuta movimientos
    def __init__(self, tablero: Board):
        self.tablero = tablero
        self.__movimientos_disponibles__ = [] # Ejemplo [3, 1] o [1, 1, 1, 1] si es doble
        self.__movimientos_restantes__ = 0 # Contador de dados restantes

    def iniciar_turno(self, dice_logic: DiceGameLogic):
        self.__movimientos_disponibles__ = dice_logic.cantidad_movimientos()
        self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

    def usar_dado(self, valor: int):
        if valor not in self.__movimientos_disponibles__:
            raise ValueError(f"El dado {valor} no está disponible")
        self.__movimientos_disponibles__.remove(valor)
        self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

    def movimientos_restantes_count(self) -> int:
        return self.__movimientos_restantes__

    def ejecutar_movimiento(self, origen, destino, color, dado):
        if self.tablero.mostrar_barra()[color]:
            raise Exception("Debe reingresar desde la barra primero")
        self.tablero.mover_ficha(origen, destino, color)
        self.usar_dado(dado)

    def ejecutar_movimiento_barra(self, destino, color, dado):
        if not self.tablero.mostrar_barra()[color]:
            raise Exception("No hay fichas en la barra")
        # El método Board.mover_desde_barra ya tiene lógica de validación
        if not self.tablero.mover_desde_barra(color, destino):
             raise Exception("Movimiento de barra fallido")
        self.usar_dado(dado)

    def ejecutar_retiro(self, casilla, dado, color):
        # Chequea si todas las fichas están en el Home Board
        home_board = range(18, 24) if color == "Blanco" else range(0, 6)
        casillas_en_juego = self.tablero.mostrar_casillas()
        for i in range(24):
            if i not in home_board and color in casillas_en_juego[i]:
                raise Exception("No se puede retirar, hay fichas fuera del Home Board")
        
        self.tablero.retirar_ficha(casilla, color)
        self.usar_dado(dado)


class BackgammonGame: # Coordina el juego completo
    def __init__(self, jugador_blanco: Player, jugador_negro: Player, turn_manager: TurnManager, move_manager: MoveManager, dice_logic: DiceGameLogic):
        self.__jugador_blanco__ = jugador_blanco
        self.__jugador_negro__ = jugador_negro
        self.__dice_logic__ = dice_logic
        self.__turnos__ = turn_manager  # Inversión de Dependencias
        self.__movimientos__ = move_manager  # Inversión de Dependencias
        self.__ganador__ = None

    def determinar_primer_turno(self):
        # Asumiendo que el dado ya fue tirado por Dice
        dado_valor = self.__dice_logic__.__dice__.__dice1__
        self.__turnos__.determinar_primer_turno(dado_valor)

    def iniciar_turno(self):
        if self.ha_terminado():
            raise Exception("¡El juego ha terminado!")
        self.__movimientos__.iniciar_turno(self.__dice_logic__)

    def finalizar_turno(self):
        if self.__movimientos__.movimientos_restantes_count() == 0:
            self.__turnos__.cambiar_turno()

    def validar_turno(self, color):
        jugador = self.__turnos__.obtener_jugador_actual()
        if not jugador or color != jugador.obtener_color():
            raise ValueError("No es el turno del jugador")
        return jugador

    def ejecutar_movimiento(self, origen, destino, color, dado):
        if self.__ganador__:
            raise Exception("Juego terminado")
        self.validar_turno(color)
        self.__movimientos__.ejecutar_movimiento(origen, destino, color, dado)

    def ejecutar_movimiento_barra(self, destino, color, dado):
        if self.__ganador__:
            raise Exception("Juego terminado")
        self.validar_turno(color)
        self.__movimientos__.ejecutar_movimiento_barra(destino, color, dado)

    def ejecutar_retiro(self, casilla, dado, color):
        if self.__ganador__:
            raise Exception("Juego terminado")
        jugador = self.validar_turno(color)
        self.__movimientos__.ejecutar_retiro(casilla, dado, color)
        jugador.incrementar_fichas_retiradas()
        if jugador.ha_ganado():
            self.__ganador__ = jugador

    def ha_terminado(self):
        return self.__ganador__ is not None