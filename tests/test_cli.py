import unittest
from core.board import Board
from core.dice import Dice, DiceGameLogic
from core.player import Player
from core.backgammongame import BackgammonGame, TurnManager, MoveManager
from cli.cli import CLI


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.jugador_blanco = Player("Blanco", "Jugador A")
        self.jugador_negro = Player("Negro", "Jugador B")
        self.tablero = Board()
        self.dado = Dice()
        self.logica_dado = DiceGameLogic(self.dado)
        self.gestor_turnos = TurnManager(self.jugador_blanco, self.jugador_negro)
        self.gestor_movimientos = MoveManager(self.tablero)
        self.juego = BackgammonGame(self.jugador_blanco, self.jugador_negro, self.gestor_turnos, self.gestor_movimientos, self.logica_dado)
        self.cli = CLI(self.juego)

    # Inicialización
    def test_inicializacion_cli(self):
        """Verifica que la CLI se inicialice correctamente con el juego."""
        self.assertIsNotNone(self.cli.__juego__)
        self.assertEqual(self.cli.__juego__, self.juego)


    # Mostrar Información
    def test_mostrar_tablero_inicial(self):
        """Verifica que la CLI muestre correctamente el tablero inicial en formato texto."""
        salida = self.cli.mostrar_tablero()
        self.assertIn("Casilla 0: Blanco, Blanco", salida)
        self.assertIn("Casilla 11: Blanco, Blanco, Blanco, Blanco, Blanco", salida)
        self.assertIn("Barra: Blanco: 0, Negro: 0", salida)

    def test_mostrar_tablero_despues_movimiento(self):
        """Verifica que la CLI actualice y muestre el tablero después de un movimiento válido."""
        self.juego.__turnos__.__jugador_actual__ = self.jugador_blanco
        self.juego.__movimientos__.__movimientos_disponibles__ = [1]
        self.juego.ejecutar_movimiento(0, 1, "Blanco", 1)
        salida = self.cli.mostrar_tablero()
        self.assertIn("Casilla 0: Blanco", salida)  # Una ficha menos
        self.assertIn("Casilla 1: Blanco", salida)  # Ficha movida

    def test_mostrar_dados_tirados(self):
        """Verifica que la CLI muestre los valores de los dados después de un tiro."""
        self.dado.establecer_valores(3, 4)
        salida = self.cli.mostrar_dados()
        self.assertIn("Dados: 3, 4", salida)

    def test_mostrar_turno_actual(self):
        """Verifica que la CLI muestre el turno del jugador actual."""
        self.juego.__turnos__.__jugador_actual__ = self.jugador_blanco
        salida = self.cli.mostrar_turno()
        self.assertIn("Turno de Blanco", salida)

    def test_mostrar_estado_juego_ganador(self):
        """Verifica que la CLI muestre un mensaje de victoria cuando el juego termina."""
        self.juego.__ganador__ = self.jugador_blanco
        salida = self.cli.mostrar_estado_juego()
        self.assertIn("¡Blanco ha ganado!", salida)

    def test_mostrar_barra_con_fichas(self):
        """Verifica que la CLI muestre la barra con fichas capturadas."""
        self.tablero.enviar_a_barra("Blanco", 0)
        salida = self.cli.mostrar_barra()
        self.assertIn("Barra: Blanco: 1, Negro: 0", salida)

    def test_mostrar_fichas_retiradas(self):
        """Verifica que la CLI muestre las fichas retiradas de cada jugador."""
        # Simular retiro en el tablero
        self.tablero.mostrar_retiradas()["Blanco"].append("Blanco")
        salida = self.cli.mostrar_fichas_retiradas()
        self.assertIn("Retiradas: Blanco: 1, Negro: 0", salida)


    # Procesar y Validar Entradas
    def test_procesar_comando_movimiento_valido(self):
        """Verifica que la CLI procese correctamente un comando de movimiento válido."""
        comando = self.cli.procesar_comando("mover 1 a 4")
        self.assertEqual(comando["tipo"], "mover")
        self.assertEqual(comando["origen"], 1)
        self.assertEqual(comando["destino"], 4)

    def test_procesar_comando_movimiento_barra(self):
        """Verifica que la CLI procese correctamente un comando de movimiento desde barra."""
        comando = self.cli.procesar_comando("mover barra a 5")
        self.assertEqual(comando["tipo"], "mover_barra")
        self.assertEqual(comando["destino"], 5)

    def test_procesar_comando_retiro(self):
        """Verifica que la CLI procese correctamente un comando de retiro."""
        comando = self.cli.procesar_comando("retirar 23")
        self.assertEqual(comando["tipo"], "retirar")
        self.assertEqual(comando["casilla"], 23)

    def test_manejar_entrada_invalida_formato(self):
        """Verifica que la CLI rechace entradas malformadas y muestre mensaje de error."""
        try:
            self.cli.procesar_comando("mover abc")
            self.fail("ValueError no fue lanzado para entrada inválida.")
        except ValueError as e:
            self.assertIn("Formato inválido", str(e))

    def test_manejar_movimiento_ilegal(self):
        """Verifica que la CLI muestre error específico cuando el movimiento es ilegal."""
        self.juego.__turnos__.__jugador_actual__ = self.jugador_blanco
        self.juego.__movimientos__.__movimientos_disponibles__ = [1]
        try:
            self.cli.ejecutar_comando("mover 0 a 12")  # Casilla bloqueada
            self.fail("Exception no fue lanzada para movimiento ilegal.")
        except Exception as e:
            self.assertIn("bloqueada", str(e))

    def test_manejar_comando_desconocido(self):
        """Verifica que la CLI responda a comandos desconocidos con un mensaje de ayuda."""
        try:
            self.cli.ejecutar_comando("xyz")
            self.fail("ValueError no fue lanzado para comando desconocido.")
        except ValueError as e:
            self.assertIn("Comando desconocido", str(e))

    def test_manejar_entrada_vacia(self):
        """Verifica que la CLI maneje entradas vacías sin errores."""
        try:
            self.cli.procesar_comando("")
            self.fail("ValueError no fue lanzado para entrada vacía.")
        except ValueError as e:
            self.assertIn("Entrada vacía", str(e))

    def test_manejar_numeros_fuera_rango(self):
        """Verifica que la CLI rechace números fuera del rango del tablero."""
        try:
            self.cli.procesar_comando("mover 25 a 26")
            self.fail("ValueError no fue lanzado para números fuera de rango.")
        except ValueError as e:
            self.assertIn("Número fuera de rango", str(e))


    # Comandos Especiales y Flujo
    def test_comando_ayuda_muestra_ayuda(self):
        """Verifica que el comando 'ayuda' muestre una lista de comandos disponibles."""
        salida = self.cli.ejecutar_comando("ayuda")
        self.assertIn("Comandos disponibles:", salida)
        self.assertIn("mover", salida)
        self.assertIn("salir", salida)

    def test_comando_salir_termina_juego(self):
        """Verifica que el comando 'salir' termine el loop de la CLI."""
        resultado = self.cli.ejecutar_comando("salir")
        self.assertTrue(resultado)  # Asumiendo que retorna True para salir

    def test_flujo_turno_completo(self):
        """Verifica que la CLI maneje un turno completo: mostrar estado, recibir input, ejecutar movimiento."""
        self.juego.__turnos__.__jugador_actual__ = self.jugador_blanco
        self.dado.establecer_valores(1, 2)
        self.juego.iniciar_turno()
        salida_inicial = self.cli.mostrar_estado_turno()
        self.assertIn("Movimientos restantes: 2", salida_inicial)
        self.cli.ejecutar_comando("mover 0 a 1")
        salida_despues = self.cli.mostrar_estado_turno()
        self.assertIn("Movimientos restantes: 1", salida_despues)

    def test_manejar_error_dado_no_disponible(self):
        """Verifica que la CLI muestre error cuando se intenta usar un dado ya usado."""
        self.juego.__turnos__.__jugador_actual__ = self.jugador_blanco
        self.juego.__movimientos__.__movimientos_disponibles__ = [3]
        try:
            self.cli.ejecutar_comando("mover 0 a 4")  # Intenta usar dado 4, no disponible
            self.fail("ValueError no fue lanzado para dado no disponible.")
        except ValueError as e:
            self.assertIn("no está disponible", str(e))

    def test_mostrar_movimientos_restantes(self):
        """Verifica que la CLI muestre cuántos movimientos quedan en el turno."""
        self.juego.__movimientos__.__movimientos_restantes__ = 2
        salida = self.cli.mostrar_movimientos_restantes()
        self.assertIn("Movimientos restantes: 2", salida)

    def test_mostrar_historial_movimientos(self):
        """Verifica que la CLI muestre un historial de movimientos realizados."""
        # Asumiendo que la CLI tiene un historial
        self.cli.__historial__.append("Movimiento: Blanco movió de 0 a 1")
        salida = self.cli.mostrar_historial()
        self.assertIn("Movimiento: Blanco movió de 0 a 1", salida)

    def test_manejar_juego_terminado_en_comando(self):
        """Verifica que la CLI bloquee comandos cuando el juego ha terminado."""
        self.juego.__ganador__ = self.jugador_blanco
        try:
            self.cli.ejecutar_comando("mover 0 a 1")
            self.fail("Exception no fue lanzada para juego terminado.")
        except Exception as e:
            self.assertIn("Juego terminado", str(e))

    def test_mostrar_mensaje_bienvenida(self):
        """Verifica que la CLI muestre un mensaje de bienvenida al iniciar."""
        salida = self.cli.mostrar_bienvenida()
        self.assertIn("Bienvenido al Backgammon", salida)