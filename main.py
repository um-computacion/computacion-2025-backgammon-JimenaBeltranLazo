from core.board import Board
from core.dice import Dice, DiceGameLogic
from core.player import Player
from core.backgammongame import BackgammonGame, TurnManager, MoveManager
from cli.cli import CLI


def main():
    # Crear jugadores
    jugador_blanco = Player("Blanco", "Jugador Blanco")
    jugador_negro = Player("Negro", "Jugador Negro")

    # Crear componentes del juego
    tablero = Board()
    dado = Dice()
    logica_dado = DiceGameLogic(dado)
    gestor_turnos = TurnManager(jugador_blanco, jugador_negro)
    gestor_movimientos = MoveManager(tablero)
    juego = BackgammonGame(jugador_blanco, jugador_negro, gestor_turnos, gestor_movimientos, logica_dado)

    # Crear CLI
    cli = CLI(juego)

    # Mostrar bienvenida
    print(cli.mostrar_bienvenida())

    # Loop principal
    while True:
        try:
            # Mostrar estado del turno
            print(cli.mostrar_estado_turno())
            print(cli.mostrar_tablero())

            # Pedir comando al usuario
            comando = input("Ingresa un comando (ayuda para ver opciones): ").strip()

            # Ejecutar comando
            resultado = cli.ejecutar_comando(comando)

            if isinstance(resultado, str):
                print(resultado)
            elif resultado:  # Si es True, salir
                print("¡Hasta luego!")
                break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()