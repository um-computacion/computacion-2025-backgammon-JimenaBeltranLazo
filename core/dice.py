import random

class Dice:

    def __init__(self):
        self.__dice1__ = None
        self.__dice2__ = None

    def tirar_dados(self):
        self.__dice1__ = random.randint(1, 6)
        self.__dice2__ = random.randint(1, 6)
        return self.__dice1__, self.__dice2__

    def establecer_valores(self, d1, d2):
        self.__dice1__ = d1
        self.__dice2__ = d2

    def es_doble(self):
        return self.__dice1__ == self.__dice2__

    def cantidad_movimientos(self):
        if self.es_doble():
            return [self.__dice1__] * 4
        return [self.__dice1__, self.__dice2__]