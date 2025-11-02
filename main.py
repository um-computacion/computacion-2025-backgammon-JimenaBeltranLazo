from cli.cli import CLI, CLICommandParser, CLIInput, CLIBuilder, CLIPresenter, CLIGameExecutor


def run_cli_app():
    # Instanciar los componentes de bajo nivel
    parser_concreto = CLICommandParser()
    input_concreto = CLIInput()

    # Crear el builder y el juego
    builder = CLIBuilder()
    nombres = input_concreto.configurar_jugadores()
    juego = builder.crear_juego(nombres)

    # Crear los componentes de presentación y ejecución
    presentador = CLIPresenter(juego)
    ejecutor = CLIGameExecutor(juego)

    # Inyectar las dependencias en CLI
    app = CLI(input=input_concreto, parser=parser_concreto, presentador=presentador, ejecutor=ejecutor)
    app.ejecutar()

def main():
    """
    Función principal que permite al usuario elegir qué versión del juego ejecutar.
    """
    while True:
        print("\n¿Qué versión del juego te gustaría ejecutar?")
        print("1. Versión de Consola")
        print("2. Versión con Pygame")
        choice = input("Por favor, elige una opción (1 o 2): ")

        if choice == '1':
            print("Iniciando la versión de consola...")
            run_cli_app()
            break
        elif choice == '2':
            print("Iniciando la versión con Pygame...")
            try:
                from pygame_ui.backgammon_pygame import run_pygame_app
                run_pygame_app()
            except ImportError:
                print("\nError: Parece que Pygame no está instalado.")
                print("Por favor, instálalo ejecutando: pip install pygame")
            break
        else:
            print("Opción no válida. Por favor, introduce 1 o 2.")


if __name__ == "__main__":
    main()