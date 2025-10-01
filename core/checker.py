class Checker:

    def __init__(self, color: str, posicion: int):
        self.__color__ = color
        self.__posicion__ = posicion
        self.__en_juego__ = True

    def mover_a(self, nueva_posicion: int):
        if not (1 <= nueva_posicion <= 24):
            raise ValueError("La posición debe estar entre 1 y 24")
        self.__posicion__ = nueva_posicion