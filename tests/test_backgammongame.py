import unittest
from core.backgammongame import BackgammonGame

class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        self.game = BackgammonGame()
        self.game.iniciar_juego()
        self.white = self.game.__players__[0]
        self.black = self.game.__players__[1]

    # Inicio de juego y estado inicial
    def test_inicio_juego(self):
        self.assertIsNotNone(self.game.obtener_jugador_actual())
        self.assertFalse(self.game.juego_terminado())
        self.assertEqual(len(self.game.board.mostrar_casillas()), 24)

    # Turnos alternados
    def test_turnos_alternados(self):
        player1 = self.game.obtener_jugador_actual()
        self.game.siguiente_turno()
        player2 = self.game.obtener_jugador_actual()
        self.assertNotEqual(player1, player2)
        self.game.siguiente_turno()
        self.assertEqual(player1, self.game.obtener_jugador_actual())

    # Movimiento legal simple
    def test_movimiento_valido(self):
        self.game.board.reiniciar()
        self.game.board.__casillas__[0] = ["Blanco"]
        self.game.dice.establecer_valores(1, 1)
        movimientos = self.game.obtener_movimientos_validos()
        if movimientos:
            resultado = self.game.jugar_turno([movimientos[0]])
            self.assertTrue(resultado)

    # Intento de movimiento inválido
    def test_movimiento_invalido(self):
        self.game.board.reiniciar()
        self.game.board.__casillas__[0] = ["Blanco"]
        self.game.dice.establecer_valores(2, 4)
        movimientos_invalidos = [(99, 100)]
        resultado = self.game.jugar_turno(movimientos_invalidos)
        self.assertFalse(resultado)

    # Captura de ficha enemiga
    def test_captura_ficha(self):
        current_player = self.game.obtener_jugador_actual()
        opponent_player = self.game.obtener_oponente()
        self.game.board.reiniciar()
        self.game.board.__casillas__[8] = [opponent_player.__color__]
        self.game.board.__casillas__[6] = [current_player.__color__]
        self.game.dice.establecer_valores(2, 4)
        resultado = self.game.jugar_turno([(6, 8)])
        self.assertTrue(resultado)
        self.assertTrue(self.game.hay_ficha_en_barra(opponent_player.__color__))

    # Movimiento desde la barra obligatorio
    def test_prioridad_barra(self):
        player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__barra__[player.__color__] = [player.__color__]
        self.game.dice.establecer_valores(3, 5)
        movimiento_no_barra = (5, 8)
        resultado = self.game.jugar_turno([movimiento_no_barra])
        self.assertFalse(resultado)

    # Tiradas dobles
    def test_tirada_doble(self):
        self.game.dice.establecer_valores(3, 3)
        movimientos = self.game.obtener_movimientos_doble()
        resultado = self.game.jugar_turno(movimientos)
        self.assertTrue(resultado)

    # Condición de victoria y ganador
    def test_victoria_y_ganador(self):
        player = self.game.obtener_jugador_actual()
        self.game.__jugador_actual__ = player
        self.game.__fichas_retiradas__ = {
            self.white.__color__: 15 if player.__color__ == "Blanco" else 0,
            self.black.__color__: 15 if player.__color__ == "Negro" else 0
        }
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.obtener_ganador(), player)

    # Reinicio del juego
    def test_reinicio_juego(self):
        self.game.reiniciar_juego()
        self.assertFalse(self.game.juego_terminado())
        self.assertIsNotNone(self.game.obtener_jugador_actual())
        self.assertEqual(len(self.game.board.mostrar_casillas()), 24)

    # Pruebas de Movimientos y Reglas
    def test_movimiento_con_varios_dados_diferentes(self):
        self.game.dice.establecer_valores(3, 5)
        self.game.board.reiniciar()
        self.game.board.__casillas__[0] = ["Blanco"]
        self.game.board.__casillas__[3] = ["Blanco"]
        movimientos = [(0, 3), (3, 8)]
        resultado = self.game.jugar_turno(movimientos)
        self.assertTrue(resultado)

    def test_movimiento_a_casilla_bloqueada(self):
        current_player = self.game.obtener_jugador_actual()
        opponent_player = self.game.obtener_oponente()
        self.game.board.reiniciar()
        self.game.board.__casillas__[15] = [opponent_player.__color__] * 2
        self.game.board.__casillas__[10] = [current_player.__color__]
        self.game.dice.establecer_valores(5, 5)
        movimiento_invalido = (10, 15)
        resultado = self.game.jugar_turno([movimiento_invalido])
        self.assertFalse(resultado)

    def test_movimiento_a_distancia_mayor_a_dado(self):
        self.game.dice.establecer_valores(2, 4)
        self.game.board.reiniciar()
        self.game.board.__casillas__[0] = ["Blanco"]
        movimiento_invalido = (0, 7)
        resultado = self.game.jugar_turno([movimiento_invalido])
        self.assertFalse(resultado)

    def test_turno_sin_movimientos_posibles(self):
        original_player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__casillas__[0] = [self.white.__color__] * 15
        self.game.dice.establecer_valores(1, 1)
        self.game.jugar_turno([])
        new_player = self.game.obtener_jugador_actual()
        self.assertNotEqual(original_player, new_player)

    # Lógica de la Barra
    def test_reingreso_desde_la_barra_exitoso(self):
        player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__barra__[player.__color__].append(player.__color__)
        self.game.dice.establecer_valores(3, 5)
        movimiento_valido = ("barra", 3)
        resultado = self.game.jugar_turno([movimiento_valido])
        self.assertTrue(resultado)
        self.assertFalse(self.game.hay_ficha_en_barra(player.__color__))

    def test_reingreso_desde_barra_casilla_bloqueada(self):
        player = self.game.obtener_jugador_actual()
        opponent = self.game.obtener_oponente()
        self.game.board.reiniciar()
        self.game.board.__barra__[player.__color__].append(player.__color__)
        self.game.board.__casillas__[4] = [opponent.__color__] * 2
        self.game.dice.establecer_valores(2, 4)
        movimiento_invalido = ("barra", 4)
        resultado = self.game.jugar_turno([movimiento_invalido])
        self.assertFalse(resultado)
        self.assertTrue(self.game.hay_ficha_en_barra(player.__color__))

    # Borne off
    def test_bornear_cuando_hay_fichas_fuera_del_cuadrante(self):
        player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__casillas__[20] = [player.__color__] * 5
        self.game.board.__casillas__[10] = [player.__color__]
        self.game.dice.establecer_valores(5, 6)
        movimiento_borne_off = (20, "borne_off")
        resultado = self.game.jugar_turno([movimiento_borne_off])
        self.assertFalse(resultado)

    def test_borne_off_con_dado_justo(self):
        player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__casillas__[22] = [player.__color__]
        self.game.dice.establecer_valores(2, 4)
        movimiento_valido = (22, "borne_off")
        resultado = self.game.jugar_turno([movimiento_valido])
        self.assertTrue(resultado)

    def test_borne_off_con_dado_sobrante(self):
        player = self.game.obtener_jugador_actual()
        self.game.board.reiniciar()
        self.game.board.__casillas__[23] = [player.__color__]
        self.game.dice.establecer_valores(6, 6)
        movimiento_valido = (23, "borne_off")
        resultado = self.game.jugar_turno([movimiento_valido])
        self.assertTrue(resultado)