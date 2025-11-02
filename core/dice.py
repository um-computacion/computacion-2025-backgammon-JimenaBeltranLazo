import random

class Dice: # Solo genera y almacena los valores de los dados
    def __init__(self):
        self.__dice1__ = None
        self.__dice2__ = None

    def tirar_dados(self):
        self.__dice1__ = random.randint(1, 6)
        self.__dice2__ = random.randint(1, 6)

    def establecer_valores(self, d1, d2):
        self.__dice1__ = d1
        self.__dice2__ = d2    

    def obtener_valores(self):
        return self.__dice1__, self.__dice2__

class DiceGameLogic: # Solo lógica del juego (dobles y movimientos)
    def __init__(self, dice: Dice):
        self.__dice__ = dice

    def es_doble(self):
        d1, d2 = self.__dice__.obtener_valores()
        return d1 == d2

    def cantidad_movimientos(self):
        d1, d2 = self.__dice__.obtener_valores()
        if self.es_doble():
            return [d1] * 4
        return [d1, d2]