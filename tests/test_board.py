import unittest
from core.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    # Inicialización
    def test_inicializacion_casillas(self):
        casillas = self.board.mostrar_casillas()
        self.assertEqual(len(casillas), 24)
        self.assertEqual(casillas[0], ["Blanco", "Blanco"])
        self.assertEqual(casillas[5], ["Negro"] * 5)
        self.assertEqual(casillas[7], ["Negro"] * 3)
        self.assertEqual(casillas[11], ["Blanco"] * 5)
        self.assertEqual(casillas[12], ["Negro"] * 5)
        self.assertEqual(casillas[16], ["Blanco"] * 3)
        self.assertEqual(casillas[18], ["Blanco"] * 5)
        self.assertEqual(casillas[23], ["Negro", "Negro"])
        
    def test_inicializacion_barra_retiradas_vacias(self):
        # Barra y retiradas deben estar vacías al inicio
        self.assertEqual(self.board.mostrar_barra(), {"Blanco": [], "Negro": []})
        self.assertEqual(self.board.mostrar_retiradas(), {"Blanco": [], "Negro": []})

    def test_mover_ficha_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(-1, 1, "Blanco")
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 24, "Blanco")

    # Movimiento de Fichas
    def test_mover_ficha_valida(self):
        # Mover ficha válida actualiza las casillas
        self.board.__casillas__[0] = ["Blanco"]
        self.board.__casillas__[1] = []
        self.board.mover_ficha(0, 1, "Blanco")
        self.assertIn("Blanco", self.board.__casillas__[1])
        self.assertNotIn("Blanco", self.board.__casillas__[0])

    def test_mover_ficha_invalida(self):
        # No se puede mover si no es legal
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "Negro") # no hay negras en 0

    def test_mover_ficha_con_captura(self):
        # Si hay una ficha enemiga sola, debe ir a la barra
        self.board.__casillas__[0] = ["Blanco"]
        self.board.__casillas__[1] = ["Negro"]
        self.board.mover_ficha(0, 1, "Blanco")
        self.assertIn("Blanco", self.board.__casillas__[1])
        self.assertIn("Negro", self.board.__barra__["Negro"])

    def test_mover_ficha_a_casilla_bloqueada(self):
        self.board.__casillas__[0] = ["Blanco"]
        self.board.__casillas__[1] = ["Negro", "Negro"]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "Blanco")

    # Barra
    def test_enviar_a_barra_valido(self):
        # Enviar ficha a la barra cuando el color coincide
        self.board.__casillas__[0] = ["Blanco"]
        resultado = self.board.enviar_a_barra("Blanco", 0)
        self.assertTrue(resultado)
        self.assertIn("Blanco", self.board.__barra__["Blanco"])
        self.assertEqual(self.board.__casillas__[0], [])

    def test_enviar_a_barra_invalido(self):
        # No debe enviar a barra si la casilla está vacía o el color es incorrecto
        self.board.__casillas__[0] = []
        self.assertFalse(self.board.enviar_a_barra("Blanco", 0))
        self.board.__casillas__[0] = ["Negro"]
        self.assertFalse(self.board.enviar_a_barra("Blanco", 0))

    def test_enviar_a_barra_fuera_de_rango(self):
        resultado = self.board.enviar_a_barra("Blanco", -1)
        self.assertFalse(resultado)
        resultado = self.board.enviar_a_barra("Blanco", 24)
        self.assertFalse(resultado)

    def test_mover_desde_barra_valido(self):
        # Mover ficha desde barra a casilla vacía
        self.board.__barra__["Blanco"].append("Blanco")
        resultado = self.board.mover_desde_barra("Blanco", 2)
        self.assertTrue(resultado)
        self.assertIn("Blanco", self.board.__casillas__[2])
        self.assertEqual(self.board.__barra__["Blanco"], [])

    def test_mover_desde_barra_invalido(self):
        # No se mueve desde barra si está vacía
        resultado = self.board.mover_desde_barra("Negro", 3)
        self.assertFalse(resultado)

    def test_mover_desde_barra_fuera_de_rango(self):
        self.board.__barra__["Blanco"].append("Blanco")
        resultado = self.board.mover_desde_barra("Blanco", -1)
        self.assertFalse(resultado)
        resultado = self.board.mover_desde_barra("Blanco", 24)
        self.assertFalse(resultado)

    # Fichas Retiradas
    def test_retirar_ficha_valida(self):
        # Retirar ficha válida la mueve a retiradas
        self.board.__casillas__[23] = ["Negro"]
        self.board.retirar_ficha(23, "Negro")
        self.assertIn("Negro", self.board.__fichas_retiradas__["Negro"])
        self.assertEqual(self.board.__casillas__[23], [])

    def test_retirar_ficha_invalida(self):
        # No se puede retirar ficha si la casilla está vacía o el color es distinto
        with self.assertRaises(ValueError):
            self.board.retirar_ficha(0, "Negro") # en 0 hay blancas al inicio

    def test_retirar_ficha_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.board.retirar_ficha(-1, "Blanco")
        with self.assertRaises(ValueError):
            self.board.retirar_ficha(24, "Negro")

    # Reinicio
    def test_reiniciar_tablero(self):
       # Tablero vuelve al estado inicial
        self.board.__casillas__[0] = []
        self.board.__barra__["Blanco"].append("Blanco")
        self.board.reiniciar()
        self.assertEqual(self.board.__casillas__[0], ["Blanco", "Blanco"])
        self.assertEqual(self.board.__barra__, {"Blanco": [], "Negro": []})