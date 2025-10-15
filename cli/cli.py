class CLI:
    def __init__(self, juego):
        self.__juego__ = juego
        self.__historial__ = [] # Registra movimientos realizados

    def mostrar_bienvenida(self):
        return "Bienvenido al Backgammon"

    def mostrar_tablero(self):
        tablero = self.__juego__.__movimientos__.tablero.mostrar_casillas()
        barra = self.__juego__.__movimientos__.tablero.mostrar_barra()
        salida = ""
        for i in range(24):
            fichas = ", ".join(tablero[i]) if tablero[i] else "Vacía"
            salida += f"Casilla {i}: {fichas}\n"
        salida += f"Barra: Blanco: {len(barra['Blanco'])}, Negro: {len(barra['Negro'])}"
        return salida

    def mostrar_dados(self):
        d1, d2 = self.__juego__.__dice_logic__.__dice__.obtener_valores()
        return f"Dados: {d1}, {d2}"

    def mostrar_turno(self):
        jugador = self.__juego__.__turnos__.obtener_jugador_actual()
        if jugador:
            return f"Turno de {jugador.obtener_color()}"
        return "Turno no determinado"

    def mostrar_estado_juego(self):
        if self.__juego__.ha_terminado():
            ganador = self.__juego__.__ganador__.obtener_color()
            return f"¡{ganador} ha ganado!"
        return "Juego en curso"

    def mostrar_barra(self):
        barra = self.__juego__.__movimientos__.tablero.mostrar_barra()
        return f"Barra: Blanco: {len(barra['Blanco'])}, Negro: {len(barra['Negro'])}"

    def mostrar_fichas_retiradas(self):
        retiradas = self.__juego__.__movimientos__.tablero.mostrar_retiradas()
        return f"Retiradas: Blanco: {len(retiradas['Blanco'])}, Negro: {len(retiradas['Negro'])}"

    def mostrar_movimientos_restantes(self):
        restantes = self.__juego__.__movimientos__.movimientos_restantes_count()
        return f"Movimientos restantes: {restantes}"

    def mostrar_estado_turno(self):
        turno = self.mostrar_turno()
        dados = self.mostrar_dados()
        movimientos = self.mostrar_movimientos_restantes()
        return f"{turno}\n{dados}\n{movimientos}"

    def mostrar_historial(self):
        if not self.__historial__:
            return "No hay movimientos en el historial"
        return "\n".join(self.__historial__)

    def procesar_comando(self, entrada):
        entrada = entrada.strip().lower()
        if not entrada:
            raise ValueError("Entrada vacía")
        partes = entrada.split()
        if len(partes) < 1:
            raise ValueError("Formato inválido")
        comando = partes[0]
        if comando == "mover":
            if len(partes) != 4 or partes[2] != "a":
                raise ValueError("Formato inválido para mover")
            origen_str = partes[1]
            destino_str = partes[3]
            try:
                destino = int(destino_str)
                if not (0 <= destino <= 23):
                    raise ValueError("Número fuera de rango")
            except ValueError:
                if destino_str.isdigit():
                    raise ValueError("Número fuera de rango")
                else:
                    raise ValueError("Formato inválido")
            if origen_str == "barra":
                return {"tipo": "mover_barra", "destino": destino}
            else:
                try:
                    origen = int(origen_str)
                    if not (0 <= origen <= 23):
                        raise ValueError("Número fuera de rango")
                except ValueError:
                    if origen_str.isdigit():
                        raise ValueError("Número fuera de rango")
                    else:
                        raise ValueError("Formato inválido")
                return {"tipo": "mover", "origen": origen, "destino": destino}
        elif comando == "retirar":
            if len(partes) != 2:
                raise ValueError("Formato inválido para retirar")
            try:
                casilla = int(partes[1])
                if not (0 <= casilla <= 23):
                    raise ValueError("Número fuera de rango")
            except ValueError:
                raise ValueError("Formato inválido")
            return {"tipo": "retirar", "casilla": casilla}
        else:
            raise ValueError("Comando desconocido")

    def ejecutar_comando(self, comando_str):
        comando_str_lower = comando_str.lower().strip()
        if comando_str_lower == "ayuda":
            return "Comandos disponibles:\nmover [origen] a [destino]\nmover barra a [destino]\nretirar [casilla]\nayuda\nsalir"
        elif comando_str_lower == "salir":
            return True
        if self.__juego__.ha_terminado():
            raise Exception("Juego terminado")
        comando = self.procesar_comando(comando_str)
        tipo = comando["tipo"]
        if tipo == "mover":
            origen = comando["origen"]
            destino = comando["destino"]
            # Asumir dado 1 por simplicidad, o calcular basado en distancia
            dado = abs(destino - origen)
            color = self.__juego__.__turnos__.obtener_jugador_actual().obtener_color()
            self.__juego__.ejecutar_movimiento(origen, destino, color, dado)
            self.__historial__.append(f"Movimiento: {color} movió de {origen} a {destino}")
        elif tipo == "mover_barra":
            destino = comando["destino"]
            dado = destino  # Asumir dado igual al destino
            color = self.__juego__.__turnos__.obtener_jugador_actual().obtener_color()
            self.__juego__.ejecutar_movimiento_barra(destino, color, dado)
            self.__historial__.append(f"Movimiento: {color} movió desde barra a {destino}")
        elif tipo == "retirar":
            casilla = comando["casilla"]
            dado = 6  # Asumir dado 6 para retiro
            color = self.__juego__.__turnos__.obtener_jugador_actual().obtener_color()
            self.__juego__.ejecutar_retiro(casilla, dado, color)
            self.__historial__.append(f"Retiro: {color} retiró de {casilla}")
        else:
            raise ValueError("Comando desconocido")
        return False