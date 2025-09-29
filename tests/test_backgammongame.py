import unittest
from core.board import Board
from core.dice import Dice
from core.player import Player
from core.backgammongame import BackgammonGame 

class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        self.player_blanco = Player("Blanco", "Jugador A")
        self.player_negro = Player("Negro", "Jugador B")
        self.board = Board()
        self.dice = Dice()
        # Inicialización del juego
        self.game = BackgammonGame(self.board, self.dice, self.player_blanco, self.player_negro)


# Inicialización y Gestión de Turnos
    def test_configuracion_inicial_del_tablero(self):
        """Verifica que el Game se inicie con el tablero en la configuración estándar."""
        self.assertEqual(len(self.game.__tablero__.mostrar_casillas()[0]), 2)
        self.assertTrue(self.game.__tablero__.mostrar_barra()["Blanco"] == [])

    def test_determinar_primer_jugador_por_dado_alto(self):
        """Verifica que el Game asigne el turno al jugador con el dado más alto."""
        # Simular tirada: Blanco (4), Negro (2).
        self.dice.establecer_valores(4, 0) # Blanco
        self.game.determinar_primer_turno() 
        self.dice.establecer_valores(2, 0) # Negro
        self.game.determinar_primer_turno() 
        
        self.assertEqual(self.game.__jugador_actual__.obtener_color(), "Blanco")

    def test_tirada_doble_y_conteo_de_cuatro_movimientos(self):
        """Verifica que una tirada doble resulte en 4 movimientos disponibles."""
        self.dice.establecer_valores(3, 3) 
        self.game.iniciar_turno()
        
        self.assertEqual(self.game.__movimientos_disponibles__, [3, 3, 3, 3])
        self.assertEqual(self.game.__movimientos_restantes__, 4)

    def test_cambio_de_turno_automatico(self):
        """Verifica que el turno cambie solo cuando los movimientos restantes son cero."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_restantes__ = 0
        self.game.finalizar_turno()

        self.assertEqual(self.game.__jugador_actual__, self.player_negro)


# Orquestación de Movimientos y Restricciones
    def test_consumo_correcto_de_dados_en_tirada_normal(self):
        """Verifica que un movimiento consuma el dado específico y actualice el estado."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [6, 1]

        # Mover de 11 a 17 (distancia 6), usando el dado 6
        self.game.ejecutar_movimiento(11, 17, "Blanco", 6) 

        self.assertEqual(self.game.__movimientos_disponibles__, [1])
        self.assertEqual(self.game.__movimientos_restantes__, 1)

    def test_prohibicion_de_movimiento_por_dado_no_disponible(self):
        """Verifica que el Game no permita movimientos con dados no tirados o ya usados."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [5, 1]
        
        # Intentar usar un dado 6
        try:
            self.game.ejecutar_movimiento(11, 17, "Blanco", 6) 
            self.fail("ValueError no fue lanzado para dado no disponible.")
        except ValueError as e:
            self.assertIn("no está disponible", str(e)) 

    def test_orquestacion_de_captura_y_envio_a_barra(self):
        """Verifica que el Game coordine la captura de fichas (blot) y el envío a la barra."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [1]
        
        # Ficha de Negro en casilla 1
        self.game.__tablero__.mostrar_casillas()[1] = ["Negro"] 
        
        self.game.ejecutar_movimiento(0, 1, "Blanco", 1) 
        
        # Verificar que la ficha Negra esté en la barra
        self.assertEqual(len(self.game.__tablero__.mostrar_barra()["Negro"]), 1)
        self.assertEqual(self.game.__tablero__.mostrar_casillas()[1], ["Blanco"])

    def test_restriccion_por_posicion_bloqueada_no_consume_dado(self):
        """Verifica que movimientos a puntos bloqueados lancen error y no consuman el dado."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [1]

        # La casilla 12 tiene 5 fichas Negras (Bloqueada en el inicio).
        try:
             self.game.ejecutar_movimiento(11, 12, "Blanco", 1)
             self.fail("ValueError no fue lanzado para posición bloqueada.")
        except ValueError as e:
            self.assertIn("bloqueada", str(e))

        # El dado debe seguir disponible
        self.assertEqual(self.game.__movimientos_disponibles__, [1])

    def test_consumo_parcial_de_dados_en_tirada_doble(self):
        """Verifica que el Game pueda consumir una cantidad parcial de dados en una tirada doble."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [2, 2, 2, 2] # Doble 2
        
        # Ejecutar 3 movimientos (usando 3 de los dados 2)
        self.game.ejecutar_movimiento(0, 2, "Blanco", 2) 
        self.game.ejecutar_movimiento(11, 13, "Blanco", 2) 
        self.game.ejecutar_movimiento(16, 18, "Blanco", 2) 

        self.assertEqual(self.game.__movimientos_disponibles__, [2])
        self.assertEqual(self.game.__movimientos_restantes__, 1)


# Reglas Especiales: Barra y Bear Off
    def test_regla_de_prioridad_de_reingreso_desde_la_barra(self):
        """Verifica que el Game fuerce el movimiento desde la barra si hay fichas allí."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__tablero__.enviar_a_barra("Blanco", 0) 
        self.game.__movimientos_disponibles__ = [6, 1]
        
        # Intento ilegal de mover ficha en tablero (11 a 12)
        try:
             self.game.ejecutar_movimiento(11, 12, "Blanco", 1) 
             self.fail("Exception no fue lanzada al intentar mover sin reingresar de barra.")
        except Exception as e:
            self.assertIn("barra", str(e)) 

    def test_reingreso_de_barra_a_casilla_bloqueada_no_consume_dado(self):
        """Verifica que el reingreso sea denegado si el punto está bloqueado, sin consumir el dado."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__tablero__.enviar_a_barra("Blanco", 0) 
        self.game.__movimientos_disponibles__ = [6]
        
        # Bloquear el punto de reingreso para el dado 6 (punto 18)
        self.game.__tablero__.mostrar_casillas()[18] = ["Negro", "Negro"]
        
        # Intentar reingresar a casilla 18, debe fallar dentro de Board
        try:
             self.game.ejecutar_movimiento_barra(18, "Blanco", 6)
             self.fail("Exception no fue lanzada para reingreso a casilla bloqueada.")
        except Exception as e:
            self.assertIn("fallido", str(e))

        self.assertEqual(self.game.__movimientos_disponibles__, [6])
        self.assertEqual(len(self.game.__tablero__.mostrar_barra()["Blanco"]), 1)

    def test_prohibicion_de_bear_off_fuera_de_home_board(self):
        """Verifica que el Game prohíba el 'bearing off' si hay fichas fuera del cuadrante de inicio."""
        self.game.__jugador_actual__ = self.player_blanco
        self.game.__movimientos_disponibles__ = [1]
        
        # El tablero se inicia con fichas de Blanco en casilla 0 (fuera del Home Board).
        try:
             self.game.ejecutar_retiro(18, 1, "Blanco")
             self.fail("Exception no fue lanzada al intentar Bear Off fuera del Home Board.")
        except Exception as e:
            self.assertIn("Home Board", str(e))

    def test_bear_off_exitoso_y_conteo_de_fichas(self):
        """Verifica que un retiro válido consuma el dado y actualice el contador del jugador."""
        self.game.__jugador_actual__ = self.player_negro
        self.game.__movimientos_disponibles__ = [6]

        casillas = self.game.__tablero__.mostrar_casillas()
    
        for i in range(24):
            casillas[i] = []
        
        casillas[5] = ["Negro"] * 15 
    
        self.game.ejecutar_retiro(5, 6, "Negro") 

        # Verificar el retiro    
        self.assertEqual(self.game.__tablero__.mostrar_retiradas()["Negro"].count("Negro"), 1)
        self.assertEqual(self.player_negro.ha_ganado(), False)
        self.assertEqual(self.game.__movimientos_disponibles__, [])


# Condición de Victoria
    def test_deteccion_de_victoria_y_bloqueo_del_juego(self):
        """Verifica que el Game detecte la victoria, marque al ganador y bloquee el flujo."""
        self.game.__jugador_actual__ = self.player_negro
        self.player_negro.__fichas_retiradas__ = 14

        # Simular el retiro de la ficha 15
        self.player_negro.incrementar_fichas_retiradas()
        
        # Forzar la verificación de victoria
        if self.player_negro.ha_ganado():
            self.game.__ganador__ = self.player_negro

        self.assertTrue(self.game.ha_terminado())
        self.assertEqual(self.game.__ganador__, self.player_negro)

        # Verificar que el juego se bloquee al intentar iniciar un nuevo turno
        try:
             self.game.iniciar_turno()
             self.fail("Exception no fue lanzada para juego terminado.")
        except Exception as e:
            self.assertIn("terminado", str(e))