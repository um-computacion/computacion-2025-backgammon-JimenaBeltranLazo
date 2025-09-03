import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    # Valores Válidos
    def test_tirada_valida(self):
        dice1, dice2 = self.dice.tirar_dados()
        self.assertIn(dice1, range(1, 7))
        self.assertIn(dice2, range(1, 7))

    # Dados No Dobles: 2 Movimientos
    def test_obtener_no_doble(self):
        self.dice.establecer_valores(1, 3)
        movimientos = self.dice.cantidad_movimientos()
        self.assertEqual(movimientos, [1, 3])
        self.assertFalse(self.dice.es_doble()) # no es doble

    # Dados Dobles: 4 Movimientos
    def test_obtener_doble(self):
        self.dice.establecer_valores(3, 3)
        movimientos = self.dice.cantidad_movimientos()
        self.assertEqual(movimientos, [3, 3, 3, 3])
        self.assertTrue(self.dice.es_doble())