from cli.cli import CLI, CLICommandParser, CLIInput, CLIBuilder, CLIPresenter, CLIGameExecutor


def main():
    # Instanciamos los componentes de bajo nivel.
    parser_concreto = CLICommandParser()
    input_concreto = CLIInput()

    # Creamos el builder y el juego
    builder = CLIBuilder()
    nombres = input_concreto.configurar_jugadores()
    juego = builder.crear_juego(nombres)

    # Creamos los componentes de presentación y ejecución
    presentador = CLIPresenter(juego)
    ejecutor = CLIGameExecutor(juego)

    # Inyectamos las dependencias en CLI
    app = CLI(input=input_concreto, parser=parser_concreto, presentador=presentador, ejecutor=ejecutor)
    app.ejecutar()


if __name__ == "__main__":
    main()