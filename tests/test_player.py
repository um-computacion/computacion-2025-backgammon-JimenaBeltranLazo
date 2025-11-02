import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(color="Negro", nombre="Lucía")

    def test_inicializacion(self):
        # Jugador debe crearse con color, nombre y sin fichas.
        self.assertEqual(self.player.__color__, "Negro")
        self.assertEqual(self.player.__nombre__, "Lucía")
        self.assertEqual(self.player.__fichas__, [])
        self.assertEqual(self.player.__fichas_retiradas__, 0) # contador

    def test_obtener_color(self):
        self.assertEqual(self.player.obtener_color(), "Negro")

    def test_obtener_nombre(self):
        self.assertEqual(self.player.obtener_nombre(), "Lucía")

    def test_agregar_ficha(self):
        self.player.agregar_ficha("F1")
        self.assertIn("F1", self.player.__fichas__) # verifica que la ficha está en la lista
        self.assertEqual(len(self.player.__fichas__), 1) # verifica que la lista tenga exactamente 1 ficha después de agregarla

    def test_contar_fichas(self):
        self.player.__fichas__ = ["F1", "F2", "F3"]
        self.assertEqual(self.player.contar_fichas(), 3)

    def test_incrementar_fichas_retiradas(self):
        # Aumenta el contador de fichas retiradas
        self.assertEqual(self.player.__fichas_retiradas__, 0)
        self.player.incrementar_fichas_retiradas()
        self.assertEqual(self.player.__fichas_retiradas__, 1)

    def test_condicion_victoria(self):
        # Jugador gana si retiró todas sus fichas (15)
        for _ in range(15):
            self.player.incrementar_fichas_retiradas()
        self.assertTrue(self.player.ha_ganado())