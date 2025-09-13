class Player:
    def __init__(self, color: str, nombre: str):
        self.__color__ = color
        self.__nombre__ = nombre
        self.__fichas__ = []
        self.__fichas_retiradas__ = 0

    def obtener_color(self) -> str:
        return self.__color__

    def obtener_nombre(self) -> str:
        return self.__nombre__

    def agregar_ficha(self, ficha: str):
        self.__fichas__.append(ficha)

    def contar_fichas(self) -> int:
        return len(self.__fichas__)

    def incrementar_fichas_retiradas(self):
        self.__fichas_retiradas__ += 1

    def ha_ganado(self) -> bool:
        return self.__fichas_retiradas__ == 15