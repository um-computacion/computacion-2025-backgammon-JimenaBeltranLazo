import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.checker = Checker(color="Negro", posicion=1)

    def test_inicio_ficha(self):
        self.assertEqual(self.checker.__color__, "Negro")
        self.assertEqual(self.checker.__posicion__, 1)
        self.assertTrue(self.checker.__en_juego__)

    def test_mover_ficha_valido(self):
        self.checker.mover_a(5)
        self.assertEqual(self.checker.__posicion__, 5)

    def test_mover_ficha_invalido(self):
        # Se intenta mover a posición fuera de rango (24 casillas en total)
        with self.assertRaises(ValueError):
            self.checker.mover_a(25)
        # Posición original no cambia
        self.assertEqual(self.checker.__posicion__, 1)

    def test_desactivar_ficha(self):
        self.checker.__en_juego__ = False # quedó capturada
        self.checker.__posicion__ = None  # ya salió del tablero
        self.assertFalse(self.checker.__en_juego__)
        self.assertIsNone(self.checker.__posicion__)