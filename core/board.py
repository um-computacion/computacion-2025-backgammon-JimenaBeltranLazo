class Board:
    
    def __init__(self):
        self.__casillas__ = self._configuracion_inicial()
        self.__barra__ = {"Blanco": [], "Negro": []}
        self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}

    def _configuracion_inicial(self):
        casillas = [[] for _ in range(24)]
        casillas[0] = ["Blanco", "Blanco"]
        casillas[11] = ["Blanco"] * 5
        casillas[16] = ["Blanco"] * 3
        casillas[18] = ["Blanco"] * 5
        casillas[23] = ["Negro", "Negro"]
        casillas[12] = ["Negro"] * 5
        casillas[7] = ["Negro"] * 3
        casillas[5] = ["Negro"] * 5
        return casillas

    def mostrar_casillas(self):
        return self.__casillas__

    def mostrar_barra(self):
        return self.__barra__

    def mostrar_retiradas(self):
        return self.__fichas_retiradas__

    def mover_ficha(self, origen, destino, color):
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise ValueError("Moviemiento ilegal. Casilla fuera de rango")
        if color not in self.__casillas__[origen]:
            raise ValueError("No hay ficha del color en la casilla de origen")
        
        # Bloqueo si casilla destino tiene 2+ fichas enemigas
        if len(self.__casillas__[destino]) >= 2 and self.__casillas__[destino][0] != color:
            raise ValueError("Movimiento ilegal. Casilla bloqueada por el oponente")
        
        # Captura si hay una sola ficha enemiga en destino
        if len(self.__casillas__[destino]) == 1 and self.__casillas__[destino][0] != color:
            ficha_capturada = self.__casillas__[destino].pop()
            self.__barra__[ficha_capturada].append(ficha_capturada)
        self.__casillas__[origen].remove(color)
        self.__casillas__[destino].append(color)

    def enviar_a_barra(self, color, casilla):
        if casilla < 0 or casilla > 23:
            return False
        if color in self.__casillas__[casilla]:
            self.__casillas__[casilla].remove(color)
            self.__barra__[color].append(color)
            return True
        return False

    def mover_desde_barra(self, color, destino):
        if destino < 0 or destino > 23:
            return False
        if self.__barra__[color]:
            self.__barra__[color].pop()
            self.__casillas__[destino].append(color)
            return True
        return False

    def retirar_ficha(self, casilla, color):
        if casilla < 0 or casilla > 23:
            raise ValueError("No hay ficha para retirar en la casilla")
        if color not in self.__casillas__[casilla]:
            raise ValueError("No hay ficha del color en la casilla")
        self.__casillas__[casilla].remove(color)
        self.__fichas_retiradas__[color].append(color)

    def reiniciar(self):
        self.__casillas__ = self._configuracion_inicial()
        self.__barra__ = {"Blanco": [], "Negro": []}
        self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}