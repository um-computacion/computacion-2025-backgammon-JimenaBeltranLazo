from core.dice import DiceGameLogic


class TurnManager: # Solo maneja el turno actual
    def __init__(self, jugador_blanco, jugador_negro):
        self.jugador_blanco = jugador_blanco
        self.jugador_negro = jugador_negro
        self.__jugador_actual__ = None
        self.__tiradas_iniciales__ = {} # Guarda tiradas iniciales de cada jugador
        self.__primer_turno_determinado__ = False

    def determinar_primer_turno(self, dado):
        if not self.__primer_turno_determinado__:
            if "Blanco" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Blanco"] = dado
            elif "Negro" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Negro"] = dado
                self.__primer_turno_determinado__ = True
                if self.__tiradas_iniciales__["Blanco"] > self.__tiradas_iniciales__["Negro"]: # Compara el valor de los dados de ambos jugadores
                    self.__jugador_actual__ = self.jugador_blanco
                elif self.__tiradas_iniciales__["Negro"] > self.__tiradas_iniciales__["Blanco"]:
                    self.__jugador_actual__ = self.jugador_negro

    def cambiar_turno(self):
        if self.__jugador_actual__ == self.jugador_blanco:
            self.__jugador_actual__ = self.jugador_negro # Cambia a jugador negro
        else:
            self.__jugador_actual__ = self.jugador_blanco

    def obtener_jugador_actual(self):
        return self.__jugador_actual__


class MoveManager: # Solo valida y ejecuta movimientos
    def __init__(self, tablero):
        self.tablero = tablero
        self.__movimientos_disponibles__ = [] # Ejemplo [3, 1] o [1, 1, 1, 1] si es doble
        self.__movimientos_restantes__ = 0 # Contador de dados restantes

    def iniciar_turno(self, dados):
        self.__movimientos_disponibles__ = dados.cantidad_movimientos()
        self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

    def usar_dado(self, valor):
        if valor not in self.__movimientos_disponibles__:
            raise ValueError(f"El dado {valor} no está disponible")
        self.__movimientos_disponibles__.remove(valor)
        self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

    def movimientos_restantes_count(self):
        return self.__movimientos_restantes__

    def ejecutar_movimiento(self, origen, destino, color, dado):
        if self.tablero.mostrar_barra()[color]:
            raise Exception("Debe reingresar desde la barra primero")
        self.tablero.mover_ficha(origen, destino, color)
        self.usar_dado(dado)

    def ejecutar_movimiento_barra(self, destino, color, dado):
        if not self.tablero.mostrar_barra()[color]:
            raise Exception("No hay fichas en la barra")
        if not self.tablero.mover_desde_barra(color, destino):
            raise Exception("Movimiento fallido")
        self.usar_dado(dado)

    def ejecutar_retiro(self, casilla, dado, color):
        # Chequea si todas las fichas están en el Home Board
        home_board = range(18, 24) if color == "Blanco" else range(0, 7)
        for i in range(24):
            if i not in home_board and color in self.tablero.mostrar_casillas()[i]:
                raise Exception("No se puede retirar, hay fichas fuera del Home Board")
        self.tablero.retirar_ficha(casilla, color)
        self.usar_dado(dado)


class BackgammonGame: # Coordina el juego completo
    def __init__(self, tablero, dados, jugador_blanco, jugador_negro):
        self.__tablero__ = tablero
        self.__dados__ = dados
        self.__dice_logic__ = DiceGameLogic(dados)
        self.__turnos__ = TurnManager(jugador_blanco, jugador_negro)
        self.__movimientos__ = MoveManager(tablero)
        self.__jugador_blanco__ = jugador_blanco
        self.__jugador_negro__ = jugador_negro
        self.__ganador__ = None

    def determinar_primer_turno(self):
        self.__turnos__.determinar_primer_turno(self.__dados__.__dice1__)

    def iniciar_turno(self):
        if self.ha_terminado():
            raise Exception("¡El juego ha terminado!")
        self.__movimientos__.iniciar_turno(self.__dice_logic__)

    def finalizar_turno(self):
        if self.__movimientos__.movimientos_restantes_count() == 0:
            self.__turnos__.cambiar_turno()

    def ejecutar_movimiento(self, origen, destino, color, dado):
        if self.__ganador__:
            raise Exception("Juego terminado")
        if color != self.__turnos__.obtener_jugador_actual().obtener_color():
            raise ValueError("No es el turno del jugador")
        self.__movimientos__.ejecutar_movimiento(origen, destino, color, dado)

    def ejecutar_movimiento_barra(self, destino, color, dado):
        if self.__ganador__:
            raise Exception("Juego terminado")
        if color != self.__turnos__.obtener_jugador_actual().obtener_color():
            raise ValueError("No es el turno del jugador")
        self.__movimientos__.ejecutar_movimiento_barra(destino, color, dado)

    def ejecutar_retiro(self, casilla, dado, color):
        if self.__ganador__:
            raise Exception("Juego terminado")
        if color != self.__turnos__.obtener_jugador_actual().obtener_color():
            raise ValueError("No es el turno del jugador")
        self.__movimientos__.ejecutar_retiro(casilla, dado, color)
        self.__turnos__.obtener_jugador_actual().incrementar_fichas_retiradas()
        if self.__turnos__.obtener_jugador_actual().ha_ganado():
            self.__ganador__ = self.__turnos__.obtener_jugador_actual()

    def ha_terminado(self):
        return self.__ganador__ is not None