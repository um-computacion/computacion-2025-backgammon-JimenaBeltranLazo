from cli.cli import CLI


def main():
    cli = CLI()
    cli.configurar_jugadores()
    cli.inicializar_juego()

    print(cli.mostrar_bienvenida())

    while True:
        try:
            print(cli.mostrar_estado_turno())
            print(cli.mostrar_tablero())
            comando = input("Ingresa un comando (ayuda para ver opciones): ").strip()
            resultado = cli.ejecutar_comando(comando)
            if isinstance(resultado, str):
                print(resultado)
            elif resultado is True:
                print("¡Hasta luego!")
                break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()