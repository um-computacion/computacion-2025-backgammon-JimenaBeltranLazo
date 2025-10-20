from core.board import Board
from core.dice import Dice, DiceGameLogic
from core.player import Player
from core.backgammongame import BackgammonGame, TurnManager, MoveManager


class CLI:
    def __init__(self):
        pass

    def configurar_jugadores(self):
        """Configura los nombres y colores de los jugadores."""
        print("🎮 Configuración de Jugadores")
        nombre1 = input("Ingresa el nombre del Jugador 1: ").strip()
        while not nombre1:
            nombre1 = input("Nombre no puede estar vacío. Ingresa el nombre del Jugador 1: ").strip()

        color1 = ""
        while color1 not in ["blanco", "negro"]:
            color1 = input(f"¿Qué color juega {nombre1}? (blanco/negro): ").strip().lower()
            if color1 not in ["blanco", "negro"]:
                print("❌ Elige 'blanco' o 'negro'.")

        color2 = "negro" if color1 == "blanco" else "blanco"
        nombre2 = input(f"Ingresa el nombre del Jugador 2 (juega con {color2}): ").strip()
        while not nombre2:
            nombre2 = input("Nombre no puede estar vacío. Ingresa el nombre del Jugador 2: ").strip()

        self.__nombre_jugador_blanco__ = nombre1 if color1 == "blanco" else nombre2
        self.__nombre_jugador_negro__ = nombre2 if color1 == "blanco" else nombre1
        print(f"✅ Jugadores configurados: {self.__nombre_jugador_blanco__} (Blanco), {self.__nombre_jugador_negro__} (Negro)")

    def inicializar_juego(self):
        # Crear jugadores con nombres configurados
        nombre_blanco = getattr(self, '__nombre_jugador_blanco__', "Jugador Blanco")
        nombre_negro = getattr(self, '__nombre_jugador_negro__', "Jugador Negro")
        self.__jugador_blanco__ = Player("Blanco", nombre_blanco)
        self.__jugador_negro__ = Player("Negro", nombre_negro)

        # Crear componentes del juego
        self.__tablero__ = Board()
        self.__dado__ = Dice()
        self.__logica_dado__ = DiceGameLogic(self.__dado__)
        self.__gestor_turnos__ = TurnManager(self.__jugador_blanco__, self.__jugador_negro__)
        self.__gestor_movimientos__ = MoveManager(self.__tablero__)
        self.__juego__ = BackgammonGame(self.__jugador_blanco__, self.__jugador_negro__, self.__gestor_turnos__, self.__gestor_movimientos__, self.__logica_dado__)

        self.__historial__ = [] # Registra movimientos realizados

    def mostrar_bienvenida(self):
        """Muestra un mensaje de bienvenida."""
        return "🎲 ¡Bienvenido al Backgammon! 🎲\nEscribe 'ayuda' para ver los comandos disponibles."

    def mostrar_tablero(self):
        """Muestra el tablero con columnas verticales alineadas y contorno bien definido."""
        tablero = self.__juego__.__movimientos__.tablero.mostrar_casillas()
        barra = self.__juego__.__movimientos__.tablero.mostrar_barra()
        retiradas = self.__juego__.__movimientos__.tablero.mostrar_retiradas()

        def render_columna(casilla, alto=5):
            if not casilla:
                return ["     "] * alto
            color = " B " if "Blanco" in casilla[0] else " N "
            fichas = [color.center(5)] * len(casilla)
            if len(fichas) > alto:
                return fichas[-alto:]
            return (["     "] * (alto - len(fichas))) + fichas

        columnas_sup = [render_columna(tablero[i], 5) for i in range(23, 11, -1)]  # 24 a 13 (0-based: 23 to 12)
        columnas_inf = [render_columna(tablero[i], 5) for i in range(0, 12)]       # 1 a 12 (0-based: 0 to 11)

        salida = "\n🎲 TABLERO DE BACKGAMMON\n"
        # Línea superior
        salida += "╔" + ("─────┬" * 11) + "─────╗\n"
        # Números superiores
        salida += "║" + "".join(f"{i:^5}│" for i in range(24, 13, -1)) + f"{13:^5}║\n"
        # Filas superiores
        for fila in range(5):
            salida += "║" + "".join(col[fila] + "│" for col in columnas_sup[:-1]) + columnas_sup[-1][fila] + "║\n"
        # Línea media
        salida += "╠" + ("─────┼" * 11) + "─────╣\n"
        # Filas inferiores
        for fila in range(5):
            salida += "║" + "".join(col[fila] + "│" for col in columnas_inf[:-1]) + columnas_inf[-1][fila] + "║\n"
        # Números inferiores
        salida += "║" + "".join(f"{i:^5}│" for i in range(1, 12)) + f"{12:^5}║\n"
        # Línea inferior
        salida += "╚" + ("─────┴" * 11) + "─────╝\n"

        salida += f"📍 Barra: B (Blancas) = {len(barra['Blanco'])}, N (Negras) = {len(barra['Negro'])}\n"
        salida += f"🏁 Retiradas: B = {len(retiradas['Blanco'])}, N = {len(retiradas['Negro'])}\n"
        return salida

    def mostrar_dados(self):
        """Muestra los valores de los dados."""
        d1, d2 = self.__juego__.__dice_logic__.__dice__.obtener_valores()
        return f"🎲 Dados: {d1}, {d2}"

    def mostrar_turno(self):
        """Muestra de quién es el turno actual."""
        jugador = self.__juego__.__turnos__.obtener_jugador_actual()
        if jugador:
            nombre = jugador.obtener_nombre()
            return f"👤 Turno de {nombre} ({jugador.obtener_color()})"
        return "⏳ Turno no determinado (tira los dados para empezar)"

    def mostrar_estado_juego(self):
        """Muestra si el juego terminó y quién ganó."""
        if self.__juego__.ha_terminado():
            ganador = self.__juego__.__ganador__.obtener_color()
            return f"🏆 ¡{ganador} ha ganado el juego! 🎉"
        return "🎮 Juego en curso"

    def mostrar_barra(self):
        """Muestra las fichas en la barra."""
        barra = self.__juego__.__movimientos__.tablero.mostrar_barra()
        return f"📍 Barra: ⚪ Blancas: {len(barra['Blanco'])}, ⚫ Negras: {len(barra['Negro'])}"

    def mostrar_fichas_retiradas(self):
        """Muestra las fichas retiradas."""
        retiradas = self.__juego__.__movimientos__.tablero.mostrar_retiradas()
        return f"🏁 Retiradas: ⚪ Blancas: {len(retiradas['Blanco'])}, ⚫ Negras: {len(retiradas['Negro'])}"

    def mostrar_movimientos_restantes(self):
        """Muestra cuántos movimientos quedan en el turno."""
        restantes = self.__juego__.__movimientos__.movimientos_restantes_count()
        return f"🔢 Movimientos restantes: {restantes}"

    def mostrar_estado_turno(self):
        """Muestra el estado completo del turno."""
        turno = self.mostrar_turno()
        dados = self.mostrar_dados()
        dados_disponibles = self.mostrar_dados_disponibles()
        movimientos = self.mostrar_movimientos_restantes()
        return f"{turno}\n{dados}\n{dados_disponibles}\n{movimientos}"
    def mostrar_dados_disponibles(self):
        """Muestra los dados disponibles para usar."""
        dados_disponibles = self.__juego__.__movimientos__.__movimientos_disponibles__
        if dados_disponibles:
            return f"🎯 Dados disponibles: {', '.join(map(str, dados_disponibles))}"
        return "❌ No hay dados disponibles"

    def mostrar_historial(self):
        """Muestra el historial de movimientos."""
        if not self.__historial__:
            return "📜 No hay movimientos en el historial aún"
        return "📜 Historial de movimientos:\n" + "\n".join(f"  • {mov}" for mov in self.__historial__)

    def procesar_comando(self, entrada):
        entrada = entrada.strip().lower()
        if not entrada:
            raise ValueError("Entrada vacía")
        partes = entrada.split()
        if len(partes) < 1:
            raise ValueError("Formato inválido")
        comando = partes[0]
        if comando == "tirar":
            if len(partes) != 1:
                raise ValueError("Formato inválido para tirar")
            return {"tipo": "tirar"}
        elif comando == "mover":
            if len(partes) != 4 or partes[2] != "a":
                raise ValueError("Formato inválido para mover")
            origen_str = partes[1]
            destino_str = partes[3]
            try:
                destino = int(destino_str)
                if not (1 <= destino <= 24):
                    raise ValueError("Número fuera de rango")
            except ValueError:
                if destino_str.isdigit():
                    raise ValueError("Número fuera de rango")
                else:
                    raise ValueError("Formato inválido")
            if origen_str == "barra":
                return {"tipo": "mover_barra", "destino": destino - 1}  # Convertir a 0-based
            else:
                try:
                    origen = int(origen_str)
                    if not (1 <= origen <= 24):
                        raise ValueError("Número fuera de rango")
                except ValueError:
                    if origen_str.isdigit():
                        raise ValueError("Número fuera de rango")
                    else:
                        raise ValueError("Formato inválido")
                return {"tipo": "mover", "origen": origen - 1, "destino": destino - 1}  # Convertir a 0-based
        elif comando == "retirar":
            if len(partes) != 2:
                raise ValueError("Formato inválido para retirar")
            try:
                casilla = int(partes[1])
                if not (1 <= casilla <= 24):
                    raise ValueError("Número fuera de rango")
            except ValueError:
                raise ValueError("Formato inválido")
            return {"tipo": "retirar", "casilla": casilla - 1}  # Convertir a 0-based
        else:
            raise ValueError("Comando desconocido")

    def tirar_dados(self):
        """Tira los dados y determina o inicia el turno."""
        if not self.__juego__.__turnos__.obtener_jugador_actual():
            # Determinar primer turno: tirar dados para ambos jugadores
            # Tiro para Blanco
            self.__juego__.__dice_logic__.__dice__.tirar_dados()
            dado_blanco = self.__juego__.__dice_logic__.__dice__.__dice1__
            self.__juego__.determinar_primer_turno()
            # Tiro para Negro
            self.__juego__.__dice_logic__.__dice__.tirar_dados()
            dado_negro = self.__juego__.__dice_logic__.__dice__.__dice1__
            self.__juego__.determinar_primer_turno()
            # Verificar si se determinó el turno
            jugador_actual = self.__juego__.__turnos__.obtener_jugador_actual()
            if jugador_actual:
                nombre_ganador = jugador_actual.obtener_nombre()
                return f"🎲 ¡Primer turno determinado! {self.__nombre_jugador_blanco__} sacó {dado_blanco}, {self.__nombre_jugador_negro__} sacó {dado_negro}. ¡{nombre_ganador} empieza!"
            else:
                return "🎲 ¡Empate en el primer tiro! Tira de nuevo."
        else:
            # Tirar dados para turno actual
            self.__juego__.__dice_logic__.__dice__.tirar_dados()
            self.__juego__.iniciar_turno()
            d1, d2 = self.__juego__.__dice_logic__.__dice__.obtener_valores()
            nombre_jugador = self.__juego__.__turnos__.obtener_jugador_actual().obtener_nombre()
            return f"🎲 ¡{nombre_jugador} tiró los dados! Salieron {d1} y {d2}. ¡Es tu turno!"

    def mover_ficha(self, origen, destino):
        """Mueve una ficha del tablero."""
        # Calcular el dado usado basado en la distancia
        distancia = abs(destino - origen)
        # Verificar qué dados están disponibles
        dados_disponibles = self.__juego__.__movimientos__.__movimientos_disponibles__
        if distancia not in dados_disponibles:
            raise ValueError(f"El dado {distancia} no está disponible")
        dado = distancia
        jugador = self.__juego__.__turnos__.obtener_jugador_actual()
        color = jugador.obtener_color()
        nombre = jugador.obtener_nombre()
        self.__juego__.ejecutar_movimiento(origen, destino, color, dado)
        self.__historial__.append(f"Movimiento: {nombre} ({color}) movió de {origen} a {destino}")
        if self.__juego__.__movimientos__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} movió ficha de casilla {origen} a {destino}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} movió ficha de casilla {origen} a {destino}! Sigue tu turno."

    def mover_desde_barra(self, destino):
        """Mueve una ficha desde la barra."""
        # Para Negro: barra a casilla 0-5 (home board del oponente)
        # Para Blanco: barra a casilla 18-23 (home board del oponente)
        jugador = self.__juego__.__turnos__.obtener_jugador_actual()
        color = jugador.obtener_color()

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
        dados_disponibles = self.__juego__.__movimientos__.__movimientos_disponibles__
        if dado not in dados_disponibles:
            raise ValueError(f"El dado {dado} no está disponible")

        nombre = jugador.obtener_nombre()
        self.__juego__.ejecutar_movimiento_barra(destino, color, dado)
        self.__historial__.append(f"Movimiento: {nombre} ({color}) movió desde barra a {destino}")
        if self.__juego__.__movimientos__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} reingresó ficha desde la barra a casilla {destino + 1}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} reingresó ficha desde la barra a casilla {destino + 1}! Sigue tu turno."

    def retirar_ficha(self, casilla):
        """Retira una ficha del tablero."""
        jugador = self.__juego__.__turnos__.obtener_jugador_actual()
        color = jugador.obtener_color()
        
        # Calcular el dado necesario para el retiro
        if color == "Blanco":
            dado = 24 - casilla  # Para Blanco, casilla 23 = dado 1, casilla 22 = dado 2, etc.
        else:  # Negro
            dado = casilla + 1   # Para Negro, casilla 0 = dado 1, casilla 1 = dado 2, etc.
        
        # Verificar que el dado esté disponible
        dados_disponibles = self.__juego__.__movimientos__.__movimientos_disponibles__
        if dado not in dados_disponibles:
            raise ValueError(f"El dado {dado} no está disponible")
        
        nombre = jugador.obtener_nombre()
        self.__juego__.ejecutar_retiro(casilla, dado, color)
        self.__historial__.append(f"Retiro: {nombre} ({color}) retiró de {casilla}")
        if self.__juego__.ha_terminado():
            return f"🏆 ¡{nombre} retiró ficha de casilla {casilla + 1}! ¡{nombre} ha ganado el juego! 🎉"
        if self.__juego__.__movimientos__.movimientos_restantes_count() == 0:
            self.__juego__.finalizar_turno()
            return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Turno terminado. ¡Pasa al siguiente!"
        return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Sigue tu turno."

    def ejecutar_comando(self, comando_str):
        comando_str_lower = comando_str.lower().strip()
        if comando_str_lower == "ayuda":
            return "📋 Comandos disponibles:\n  🎲 tirar - Tira los dados\n  ♟️  mover [origen] a [destino] - Mueve ficha\n  🔄 mover barra a [destino] - Reingresa desde barra\n  🏁 retirar [casilla] - Retira ficha\n  ❓ ayuda - Muestra esta ayuda\n  🚪 salir - Sale del juego"
        elif comando_str_lower == "salir":
            return True
        if self.__juego__.ha_terminado():
            raise Exception("El juego ya terminó. ¡Felicidades al ganador!")
        comando = self.procesar_comando(comando_str)
        tipo = comando["tipo"]
        if tipo == "tirar":
            return self.tirar_dados()
        elif tipo == "mover":
            return self.mover_ficha(comando["origen"], comando["destino"])
        elif tipo == "mover_barra":
            return self.mover_desde_barra(comando["destino"])
        elif tipo == "retirar":
            return self.retirar_ficha(comando["casilla"])
        else:
            raise ValueError("Comando desconocido. Escribe 'ayuda' para ver opciones.")
        return False