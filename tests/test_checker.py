import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.checker = Checker(color="Negro", posicion=1)

    def test_inicio_ficha(self):
        self.assertEqual(self.checker.color, "Negro")
        self.assertEqual(self.checker.posicion, 1)
        self.assertTrue(self.checker.en_juego)

    def test_mover_ficha_valido(self):
        self.checker.mover_a(5)
        self.assertEqual(self.checker.posicion, 5)

    def test_mover_ficha_invalido(self):
        # Se intenta mover a posición fuera de rango (24 casillas en total)
        with self.assertRaises(ValueError):
            self.checker.mover_a(25)
        # Posición original no cambia
        self.assertEqual(self.checker.posicion, 1)

    def test_desactivar_ficha(self):
        self.checker.en_juego = False # quedó capturada
        self.checker.posicion = None  # ya salió del tablero
        self.assertFalse(self.checker.en_juego)
        self.assertIsNone(self.checker.posicion)