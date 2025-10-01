class BackgammonGame:

    def __init__(self, tablero, dados, jugador_blanco, jugador_negro):
        self.__tablero__ = tablero
        self.__dados__ = dados
        self.__jugador_blanco__ = jugador_blanco
        self.__jugador_negro__ = jugador_negro
        self.__jugador_actual__ = None
        self.__movimientos_disponibles__ = [] # Ejemplo [3, 1] o [1, 1, 1, 1] si es doble
        self.__movimientos_restantes__ = 0 # Contador de dados restantes
        self.__ganador__ = None
        self.__primer_turno_determinado__ = False
        self.__tiradas_iniciales__ = {} # Guarda tiradas iniciales de cada jugador

    def determinar_primer_turno(self):
        if not self.__primer_turno_determinado__:
            tirada_inicial = self.__dados__.__dice1__
            if "Blanco" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Blanco"] = tirada_inicial
            elif "Negro" not in self.__tiradas_iniciales__:
                self.__tiradas_iniciales__["Negro"] = tirada_inicial
                self.__primer_turno_determinado__ = True
                if self.__tiradas_iniciales__["Blanco"] > self.__tiradas_iniciales__["Negro"]: # Compara el valor de los dados de ambos jugadores
                    self.__jugador_actual__ = self.__jugador_blanco__
                elif self.__tiradas_iniciales__["Negro"] > self.__tiradas_iniciales__["Blanco"]:
                    self.__jugador_actual__ = self.__jugador_negro__

    def iniciar_turno(self):
        if self.ha_terminado():
            raise Exception("¡El juego ha terminado!")
        self.__movimientos_disponibles__ = self.__dados__.cantidad_movimientos()
        self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

    def finalizar_turno(self):
        if self.__movimientos_restantes__ == 0:
            if self.__jugador_actual__ == self.__jugador_blanco__:
                self.__jugador_actual__ = self.__jugador_negro__ # Cambia a jugador Negro
            else:
                self.__jugador_actual__ = self.__jugador_blanco__

    def ejecutar_movimiento(self, origen, destino, color, dado):
        if self.__ganador__ is not None:
            raise Exception("Juego terminado")
        if color != self.__jugador_actual__.obtener_color():
            raise ValueError("No es el turno del jugador")
        if dado not in self.__movimientos_disponibles__:
            raise ValueError(f"El dado {dado} no está disponible")
        if self.__tablero__.mostrar_barra()[color]:
            raise Exception("Debe reingresar desde la barra primero")
        try:
            self.__tablero__.mover_ficha(origen, destino, color)
            self.__movimientos_disponibles__.remove(dado)
            self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
        except ValueError as e:
            raise e

    def ejecutar_movimiento_barra(self, destino, color, dado):
        if self.__ganador__ is not None:
            raise Exception("Juego terminado")
        if color != self.__jugador_actual__.obtener_color():
            raise ValueError("No es el turno del jugador")
        if dado not in self.__movimientos_disponibles__:
            raise ValueError(f"El dado {dado} no está disponible")
        if not self.__tablero__.mostrar_barra()[color]:
            raise Exception("No hay fichas en la barra")
        try:
            if not self.__tablero__.mover_desde_barra(color, destino):
                raise Exception("Movimiento fallido")
            self.__movimientos_disponibles__.remove(dado)
            self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
        except Exception as e:
            raise e

    def ejecutar_retiro(self, casilla, dado, color):
        if self.__ganador__ is not None:
            raise Exception("Juego terminado")
        if color != self.__jugador_actual__.obtener_color():
            raise ValueError("No es el turno del jugador")
        if dado not in self.__movimientos_disponibles__:
            raise ValueError(f"El dado {dado} no está disponible")
        # Chequea si todas las fichas están en el Home Board
        home_board = range(18, 24) if color == "Blanco" else range(0, 7) 
        for i in range(24):
            if i not in home_board and color in self.__tablero__.mostrar_casillas()[i]:
                raise Exception("No se puede retirar, hay fichas fuera del Home Board")
        try:
            self.__tablero__.retirar_ficha(casilla, color)
            self.__jugador_actual__.incrementar_fichas_retiradas()
            self.__movimientos_disponibles__.remove(dado)
            self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
            if self.__jugador_actual__.ha_ganado():
                self.__ganador__ = self.__jugador_actual__
        except ValueError as e:
            raise e

    def ha_terminado(self):
        return self.__ganador__ is not None