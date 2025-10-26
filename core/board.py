class SquareManager: # Solo gestiona las 24 casillas del tablero
    def __init__(self):
        self.__casillas__ = self._configuracion_inicial()
        
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
    
    def mostrar(self):
        return self.__casillas__
    
    def mover_ficha(self, origen, destino, color):
        self.__casillas__[origen].remove(color)
        self.__casillas__[destino].append(color)

    def retirar_ficha(self, casilla, color):
        self.__casillas__[casilla].remove(color)

    def hay_ficha(self, casilla, color):
        return color in self.__casillas__[casilla]
    
    def casilla_bloqueada(self, destino, color):
        fichas = self.__casillas__[destino]
        return len(fichas) >= 2 and fichas[0] != color
        
    def enemigo_solo_en_destino(self, destino, color):
        fichas = self.__casillas__[destino]
        return len(fichas) == 1 and fichas[0] != color
    
    def capturar_en_destino(self, destino):
        return self.__casillas__[destino].pop()
    
class BarManager: # Solo gestiona las fichas capturadas en la barra
    def __init__(self):
        self.__barra__ = {"Blanco": [], "Negro": []}

    def enviar_a_barra(self, color):
        self.__barra__[color].append(color)

    def mover_desde_barra(self, color):
        if self.__barra__[color]:
            return self.__barra__[color].pop()
        return None
    
    def mostrar(self):
        return self.__barra__

class Board: # Coordina el tablero, la barra y aplica las reglas de movimiento
    def __init__(self):
        self.__casillas__ = SquareManager()
        self.__barra__ = BarManager()
        self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}

    def mostrar_casillas(self):
        return self.__casillas__.mostrar()
    
    def mostrar_barra(self):
        return self.__barra__.mostrar()

    def mostrar_retiradas(self):
        return self.__fichas_retiradas__

    def mover_ficha(self, origen, destino, color):
        if not (0 <= origen <= 23 and 0 <= destino <= 23):
            raise ValueError("Moviemiento ilegal. Casilla fuera de rango")
        if not self.__casillas__.hay_ficha(origen, color):
            raise ValueError("No hay ficha del color en la casilla de origen")
        if self.__casillas__.casilla_bloqueada(destino, color): # Bloqueo si casilla destino tiene 2+ fichas enemigas
            raise ValueError("Movimiento ilegal. Casilla bloqueada por el oponente")
        
        # Captura si hay una sola ficha enemiga en destino
        if self.__casillas__.enemigo_solo_en_destino(destino, color):
            ficha_capturada = self.__casillas__.capturar_en_destino(destino)
            self.__barra__.enviar_a_barra(ficha_capturada)

        self.__casillas__.mover_ficha(origen, destino, color)

    def enviar_a_barra(self, color, casilla):
        if not (0 <= casilla <= 23):
            return False
        if self.__casillas__.hay_ficha(casilla, color):
            self.__casillas__.retirar_ficha(casilla, color)
            self.__barra__.enviar_a_barra(color)
            return True
        return False

    def mover_desde_barra(self, color, destino):
        if not (0 <= destino <= 23):
            return False
        if self.__casillas__.casilla_bloqueada(destino, color):
            return False
        # Captura si hay una sola ficha enemiga en el destino
        if self.__casillas__.enemigo_solo_en_destino(destino, color):
            ficha_capturada = self.__casillas__.capturar_en_destino(destino)
            self.__barra__.enviar_a_barra(ficha_capturada)
        ficha = self.__barra__.mover_desde_barra(color)
        if ficha:
            self.__casillas__.mostrar()[destino].append(ficha)
            return True
        return False

    def retirar_ficha(self, casilla, color):
        if not (0 <= casilla <= 23):
            raise ValueError("No hay ficha para retirar en la casilla")
        if not self.__casillas__.hay_ficha(casilla, color):
            raise ValueError("No hay ficha del color en la casilla")
        self.__casillas__.retirar_ficha(casilla, color)
        self.__fichas_retiradas__[color].append(color)

    def reiniciar(self):
        self.__casillas__ = SquareManager()
        self.__barra__ = BarManager()
        self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}