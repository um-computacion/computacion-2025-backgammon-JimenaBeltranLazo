from core.board import Board
from core.dice import Dice, DiceGameLogic
from core.player import Player
from core.backgammongame import BackgammonGame, TurnManager, MoveManager


class CLIBuilder: # Se encarga solo de construir la instancia completa del juego
    def crear_juego(self, nombres):
        """Crea una instancia completa del juego."""
        jugador_blanco = Player("Blanco", nombres["blanco"])
        jugador_negro = Player("Negro", nombres["negro"])
        tablero = Board()
        dados = Dice()
        logica_dado = DiceGameLogic(dados)
        gestor_turnos = TurnManager(jugador_blanco, jugador_negro)
        gestor_movimientos = MoveManager(tablero)
        return BackgammonGame(jugador_blanco, jugador_negro, gestor_turnos, gestor_movimientos, logica_dado)


class CLIInput: # Se encarga solo de la entrada de datos del usuario
    def __init__(self):
        self.__gestor_entrada__ = input

    def configurar_jugadores(self):
        """Configura los nombres y colores de los jugadores."""
        print("Configuracion de Jugadores")
        nombre1 = self.__gestor_entrada__("Ingresa el nombre del Jugador 1: ").strip()
        while not nombre1:
            nombre1 = self.__gestor_entrada__("Nombre no puede estar vacío. Ingresa el nombre del Jugador 1: ").strip()
        color1 = ""
        while color1 not in ["blanco", "negro"]:
            color1 = self.__gestor_entrada__(f"¿Qué color juega {nombre1}? (blanco/negro): ").strip().lower()
            if color1 not in ["blanco", "negro"]:
                print("❌ Elige 'blanco' o 'negro'.")
        color2 = "negro" if color1 == "blanco" else "blanco"
        nombre2 = self.__gestor_entrada__(f"Ingresa el nombre del Jugador 2 (juega con {color2}): ").strip()
        while not nombre2:
            nombre2 = self.__gestor_entrada__("Nombre no puede estar vacío. Ingresa el nombre del Jugador 2: ").strip()
        return {
            "blanco": nombre1 if color1 == "blanco" else nombre2,
            "negro": nombre2 if color1 == "blanco" else nombre1
        }

    def leer_comando(self):
        return self.__gestor_entrada__("Ingresa un comando: ").strip()


class CLICommandParser: # Se encarga solo de interpretar y validar los comandos del usuario
    def __init__(self):
        # TABLA DE REGISTRO DE COMANDOS
        # Cada comando mapea a una función (handler) que recibe las partes y devuelve el diccionario
        # Las funciones manejan la validación específica
        self.__registro_comando__ = {
            "tirar": self.parse_tirar,
            "mover": self.parse_mover,
            "retirar": self.parse_retirar,
            "ayuda": self.parse_control,
            "salir": self.parse_control,
        }

    # MÉTODO DESPACHADOR
    def parsear(self, entrada):
        entrada = entrada.strip().lower()
        if not entrada:
            raise ValueError("Entrada vacía")
        partes = entrada.split()
        comando_base = partes[0]
        manejador = self.__registro_comando__.get(comando_base)
        if manejador:
            # Llama al manejador específico y le pasa todas las partes.
            return manejador(partes)
        else:
            raise ValueError("Comando desconocido")

    # Responsabilidad Única para 'tirar'
    def parse_tirar(self, partes):
        if len(partes) != 1:
            raise ValueError("Formato inválido para tirar")
        return {"tipo": "tirar"}

    # Responsabilidad Única para 'mover'
    def parse_mover(self, partes):
        # Toda la lógica de validación de 'mover' se mueve aquí
        if len(partes) != 4 or partes[2] != "a":
            raise ValueError("Formato inválido para mover")
        # Lógica de extracción y validación de origen/destino
        origen_str, destino_str = partes[1], partes[3]
        def validar_casilla(s):
            try:
                n = int(s)
                if not (1 <= n <= 24):
                    raise ValueError("Número fuera de rango")
                return n - 1
            except ValueError:
                raise ValueError("Formato inválido: la casilla debe ser un número entre 1 y 24.")
        destino = validar_casilla(destino_str)
        if origen_str == "barra":
            return {"tipo": "mover_barra", "destino": destino}
        else:
            origen = validar_casilla(origen_str)
            return {"tipo": "mover", "origen": origen, "destino": destino}

    # Responsabilidad Única para 'retirar'
    def parse_retirar(self, partes):
        # Toda la lógica de validación de 'retirar' se mueve aquí
        if len(partes) != 2:
            raise ValueError("Formato inválido para retirar")
        try:
            casilla = int(partes[1])
            if not (1 <= casilla <= 24):
                raise ValueError("Número fuera de rango")
        except ValueError:
            raise ValueError("Formato inválido")
        return {"tipo": "retirar", "casilla": casilla - 1}

    # Responsabilidad Única para comandos simples
    def parse_control(self, partes):
        if len(partes) != 1:
             raise ValueError(f"Formato inválido para {partes[0]}")
        return {"tipo": partes[0]}


class CLIPresenter: # Se encarga solo de mostrar el estado visual del juego
    def __init__(self, juego):
        self.__juego__ = juego

    def mostrar_bienvenida(self):
        return "🎲 ¡Bienvenido al Backgammon! 🎲\nEscribe 'ayuda' para ver los comandos disponibles."

    def mostrar_tablero(self):
        tablero = self.__juego__.obtener_estado_tablero()
        barra = self.__juego__.obtener_estado_barra()
        retiradas = self.__juego__.obtener_estado_retiradas()

        def render_columna(casilla, alto=5):
            if not casilla:
                return ["     "] * alto
            color = " B " if "Blanco" in casilla[0] else " N "
            fichas = [color.center(5)] * len(casilla)
            if len(fichas) > alto:
                return fichas[-alto:]
            return (["     "] * (alto - len(fichas))) + fichas
        columnas_sup = [render_columna(tablero[i], 5) for i in range(23, 11, -1)]
        columnas_inf = [render_columna(tablero[i], 5) for i in range(0, 12)]

        salida = "\n TABLERO DE BACKGAMMON\n"
        salida += "╔" + ("─────┬" * 11) + "─────╗\n"
        salida += "║" + "".join(f"{i:^5}│" for i in range(24, 13, -1)) + f"{13:^5}║\n"
        for fila in range(5):
            salida += "║" + "".join(col[fila] + "│" for col in columnas_sup[:-1]) + columnas_sup[-1][fila] + "║\n"
        salida += "╠" + ("─────┼" * 11) + "─────╣\n"
        for fila in range(5):
            salida += "║" + "".join(col[fila] + "│" for col in columnas_inf[:-1]) + columnas_inf[-1][fila] + "║\n"
        salida += "║" + "".join(f"{i:^5}│" for i in range(1, 12)) + f"{12:^5}║\n"
        salida += "╚" + ("─────┴" * 11) + "─────╝\n"
        salida += f"📍 Barra: B (Blancas) = {len(barra['Blanco'])}, N (Negras) = {len(barra['Negro'])}\n"
        salida += f"🏁 Retiradas: B = {len(retiradas['Blanco'])}, N = {len(retiradas['Negro'])}\n"
        return salida

    def mostrar_estado_turno(self):
        jugador = self.__juego__.obtener_jugador_actual()
        if not jugador:
            return "⏳ Turno no determinado (tira los dados para empezar)"
        nombre = jugador.obtener_nombre()
        color = jugador.obtener_color()
        d1, d2 = self.__juego__.obtener_valores_dados()
        dados_disp = self.__juego__.obtener_dados_disponibles()
        movimientos = self.__juego__.movimientos_restantes_count()
        return (
            f"👤 Turno de {nombre} ({color})\n"
            f"🎲 Dados: {d1}, {d2}\n"
            f"🎯 Dados disponibles: {', '.join(map(str, dados_disp)) if dados_disp else '❌ No hay dados disponibles'}\n"
            f"🔢 Movimientos restantes: {movimientos}"
        )

    def mostrar_historial(self, historial):
        if not historial:
            return "📜 No hay movimientos en el historial aún"
        return "📜 Historial de movimientos:\n" + "\n".join(f"  • {mov}" for mov in historial)

    def mostrar_estado_juego(self):
        if self.__juego__.ha_terminado():
            ganador = self.__juego__.obtener_ganador().obtener_color()
            return f"🏆 ¡{ganador} ha ganado el juego! 🎉"
        return "🎮 Juego en curso"

    def mostrar_ayuda(self):
        return (
            " Comandos disponibles:\n"
            "  🎲 tirar - Tira los dados\n"
            "  ♟️  mover [origen] a [destino] - Mueve ficha\n"
            "  🔄 mover barra a [destino] - Reingresa desde barra\n"
            "  🏁 retirar [casilla] - Retira ficha\n"
            "  ❓ ayuda - Muestra esta ayuda\n"
            "  🚪 salir - Sale del juego"
        )


class CLIGameExecutor: # Se encarga solo de ejecutar las acciones del juego según el comando recibido
    def __init__(self, juego):
        self.__juego__ = juego
        self.__historial__ = []
        # Diccionario de mapeo
        self.__manejadores_comando__ = {
            "tirar": lambda cmd: self._tirar_dados(),
            "mover": lambda cmd: self._mover_ficha(cmd["origen"], cmd["destino"]),
            "mover_barra": lambda cmd: self._mover_desde_barra(cmd["destino"]),
            "retirar": lambda cmd: self._retirar_ficha(cmd["casilla"])
        }

    def ejecutar(self, comando):
        tipo = comando["tipo"]
        # Buscar el manejador en el diccionario
        manejador = self.__manejadores_comando__.get(tipo)
        if manejador:
            return manejador(comando)
        else:
            raise ValueError(f"Comando de juego desconocido: {tipo}")

    def obtener_historial(self):
        return self.__historial__

    def _tirar_dados(self):
        if not self.__juego__.obtener_jugador_actual():
            dado_blanco, dado_negro = self.__juego__.tirar_dados_primer_turno()
            jugador_actual = self.__juego__.obtener_jugador_actual()
            if jugador_actual:
                nombre_ganador = jugador_actual.obtener_nombre()
                nombre_blanco = self.__juego__.obtener_jugador_por_color("Blanco").obtener_nombre()
                nombre_negro = self.__juego__.obtener_jugador_por_color("Negro").obtener_nombre()
                return f"🎲 ¡Primer turno determinado! {nombre_blanco} sacó {dado_blanco}, {nombre_negro} sacó {dado_negro}. ¡{nombre_ganador} empieza!\n\nAhora tira los dados para comenzar tu turno."
            else:
                return "🎲 ¡Empate en el primer tiro! Tira de nuevo."
        else:
            self.__juego__.tirar_dados_turno_actual()
            d1, d2 = self.__juego__.obtener_valores_dados()
            nombre_jugador = self.__juego__.obtener_jugador_actual().obtener_nombre()
            return f"🎲 ¡{nombre_jugador} tiró los dados! Salieron {d1} y {d2}. ¡Es tu turno!"

    def _mover_ficha(self, origen, destino):
        jugador = self.__juego__.obtener_jugador_actual()
        color = jugador.obtener_color()
        nombre = jugador.obtener_nombre()

        # Calcular el dado usado basado en la distancia
        distancia = abs(destino - origen)
        dados_disponibles = self.__juego__.obtener_dados_disponibles()
        if distancia not in dados_disponibles:
            raise ValueError(f"El dado {distancia} no está disponible")
        dado = distancia
        try:
            self.__juego__.ejecutar_movimiento(origen, destino, color, dado)
        except Exception as e:
            raise ValueError(str(e))
        self.__historial__.append(f"Movimiento: {nombre} ({color}) movió de {origen + 1} a {destino + 1}")
        if self.__juego__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} movió ficha de casilla {origen + 1} a {destino + 1}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} movió ficha de casilla {origen + 1} a {destino + 1}! Sigue tu turno."

    def _mover_desde_barra(self, destino):
        jugador = self.__juego__.obtener_jugador_actual()
        color = jugador.obtener_color()
        nombre = jugador.obtener_nombre()

        # Para Negro: barra a casilla 0-5 (home board del oponente)
        # Para Blanco: barra a casilla 18-23 (home board del oponente)
        # Validar destino válido para reingreso desde barra
        if color == "Blanco":
            if not (0 <= destino <= 5):
                raise ValueError("Desde la barra, Blanco solo puede reingresar en casillas 1-6")
        else:  # Negro
            if not (18 <= destino <= 23):
                raise ValueError("Desde la barra, Negro solo puede reingresar en casillas 24-19")
        # Calcular el dado necesario basado en el destino
        if color == "Blanco":
            dado = destino + 1  # Para Blanco, casilla 0 = dado 1, casilla 1 = dado 2, etc.
        else:  # Negro
            dado = 24 - destino  # Para Negro, casilla 23 = dado 1, casilla 22 = dado 2, etc.
        # Verificar que el dado esté disponible
        dados_disponibles = self.__juego__.obtener_dados_disponibles()
        if dado not in dados_disponibles:
            raise ValueError(f"El dado {dado} no está disponible")
        try:
            self.__juego__.ejecutar_movimiento_barra(destino, color, dado)
        except Exception as e:
            raise ValueError(str(e))
        self.__historial__.append(f"Movimiento: {nombre} ({color}) movió desde barra a {destino + 1}")
        if self.__juego__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} reingresó ficha desde la barra a casilla {destino + 1}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} reingresó ficha desde la barra a casilla {destino + 1}! Sigue tu turno."

    def _retirar_ficha(self, casilla):
        jugador = self.__juego__.obtener_jugador_actual()
        color = jugador.obtener_color()
        nombre = jugador.obtener_nombre()
        
        # Calcular el dado necesario para el retiro
        if color == "Blanco":
            dado = 24 - casilla  # Para Blanco, casilla 23 = dado 1, casilla 22 = dado 2, etc.
        else:  # Negro
            dado = casilla + 1   # Para Negro, casilla 0 = dado 1, casilla 1 = dado 2, etc.
        # Verificar que el dado esté disponible
        dados_disponibles = self.__juego__.obtener_dados_disponibles()
        if dado not in dados_disponibles:
            raise ValueError(f"El dado {dado} no está disponible")
        try:
            self.__juego__.ejecutar_retiro(casilla, dado, color)
        except Exception as e:
            raise ValueError(str(e))
        self.__historial__.append(f"Retiro: {nombre} ({color}) retiró de {casilla + 1}")
        if self.__juego__.ha_terminado():
            return f"🏆 ¡{nombre} retiró ficha de casilla {casilla + 1}! ¡{nombre} ha ganado el juego! 🎉"
        if self.__juego__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Sigue tu turno."


class CLI: # Se encarga de orquestar el flujo general del juego en la interfaz CLI
    def __init__(self, input, parser, presentador, ejecutor):
        self.__input__ = input
        self.__parser__ = parser
        self.__presentador__ = presentador
        self.__ejecutor__ = ejecutor

    def ejecutar(self):
        print(self.__presentador__.mostrar_bienvenida())
        print("\n🎯 Ahora vamos a determinar el turno inicial tirando los dados.")
        while True:
            try:
                entrada = self.__input__.leer_comando()
                comando = self.__parser__.parsear(entrada)
                # Interceptar comandos de control antes de delegar
                if comando["tipo"] == "ayuda":
                    print(self.__presentador__.mostrar_ayuda())
                    print()  # Línea en blanco para separación
                    continue
                elif comando["tipo"] == "salir":
                    print("¡Gracias por jugar Backgammon!")
                    break
                # Ejecutar comando de juego
                resultado = self.__ejecutor__.ejecutar(comando)
                print(resultado)
                print()
                print(self.__presentador__.mostrar_tablero())
                print()
                print(self.__presentador__.mostrar_estado_turno())
                print()
                print(self.__presentador__.mostrar_historial(self.__ejecutor__.obtener_historial()))
                print()
                print(self.__presentador__.mostrar_estado_juego())
                print()

            except Exception as e:
                print(f"⚠️ Error: {e}")
                print()  # Línea en blanco después del error