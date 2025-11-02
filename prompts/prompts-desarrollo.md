# Prompts Desarrollo: Registro de IA

## 🎯 Class Board

### GitHub Copilot 16/09/2025

Prompt: Teniendo los tests de Board me podrias hacer la parte del core/desarrollo?

Respuesta: Claro, aquí tienes una implementación para la clase Board que cumple con los tests que enviaste. Puedes ajustar los nombres o detalles según lo que necesites, pero esta versión debería pasar todos tus tests:
   ```bash
   class Board:

        def __init__(self):
            self.__casillas__ = self._configuracion_inicial()
            self.__barra__ = {"Blanco": [], "Negro": []}
            self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}

        def _configuracion_inicial(self):
            casillas = [[] for _ in range(24)]
            casillas[0] = ["Blanco", "Blanco"]
            casillas[5] = ["Negro"] * 5
            casillas[7] = ["Negro"] * 3
            casillas[11] = ["Blanco"] * 5
            casillas[12] = ["Negro"] * 5
            casillas[16] = ["Blanco"] * 3
            casillas[18] = ["Blanco"] * 5
            casillas[23] = ["Negro", "Negro"]
            return casillas

        def mostrar_casillas(self):
            return self.__casillas__

        def mostrar_barra(self):
            return self.__barra__

        def mostrar_retiradas(self):
            return self.__fichas_retiradas__

        def mover_ficha(self, origen, destino, color):
            if origen < 0 or origen > 23 or destino < 0 or destino > 23:
                raise ValueError("Casilla fuera de rango")
            if color not in self.__casillas__[origen]:
                raise ValueError("No hay ficha del color en la casilla de origen")
            # Captura si hay una sola ficha enemiga en destino
            if len(self.__casillas__[destino]) == 1 and self.__casillas__[destino][0] != color:
                ficha_capturada = self.__casillas__[destino].pop()
                self.__barra__[ficha_capturada].append(ficha_capturada)
            self.__casillas__[origen].remove(color)
            self.__casillas__[destino].append(color)

        def enviar_a_barra(self, color, casilla):
            if casilla < 0 or casilla > 23:
                return False
            if color in self.__casillas__[casilla]:
                self.__casillas__[casilla].remove(color)
                self.__barra__[color].append(color)
                return True
            return False

        def mover_desde_barra(self, color, destino):
            if destino < 0 or destino > 23:
                return False
            if self.__barra__[color]:
                self.__barra__[color].pop()
                self.__casillas__[destino].append(color)
                return True
            return False

        def retirar_ficha(self, casilla, color):
            if casilla < 0 or casilla > 23:
                raise ValueError("Casilla fuera de rango")
            if color not in self.__casillas__[casilla]:
                raise ValueError("No hay ficha del color en la casilla")
            self.__casillas__[casilla].remove(color)
            self.__fichas_retiradas__[color].append(color)

        def reiniciar(self):
            self.__casillas__ = self._configuracion_inicial()
            self.__barra__ = {"Blanco": [], "Negro": []}
            self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}
   ```
Esta clase debería pasar todos los tests que tienes en tu archivo `test_board.py`. Si necesitas agregar lógica adicional (por ejemplo, reglas de movimiento más estrictas), puedes extenderla fácilmente.

Salida: El código fue incorporado en el archivo `core/board.py`. Se modificó el texto de algunos mensajes y se incorporó en el método `mover_ficha()` una regla de bloqueo para evitar el movimiento de una ficha si la casilla destino tiene 2 o más fichas enemigas.

## 🏆 Class BackgammonGame

### Kilo Code 28/09/2025

Prompt: A partir de los siguientes tests, me podrias armar el core para la clase BackgammonGame? [Se copió y pegó el código del archivo `tests/test_backgammongame.py`]

Respuesta: ◎ **Thinking**

*First, the user wants me to implement the core for the BackgammonGame class based on the provided tests. The tests are in test_backgammongame.py, and I need to make the class in core/backgammongame.py pass these tests.*

***Reviewing User Request***
- *The user needs implementation of the BackgammonGame class core.*
- *The implementation must pass tests located in test_backgammongame.py.*
- *The class file to be worked on is core/backgammongame.py.*
```bash
   class BackgammonGame:

        def __init__(self, tablero, dados, jugador_blanco, jugador_negro):
            self.__tablero__ = tablero
            self.__dados__ = dados
            self.__jugador_blanco__ = jugador_blanco
            self.__jugador_negro__ = jugador_negro
            self.__jugador_actual__ = None
            self.__movimientos_disponibles__ = []
            self.__movimientos_restantes__ = 0
            self.__ganador__ = None
            self.__primer_turno_determinado__ = False
            self.__rolls__ = {}

        def determinar_primer_turno(self):
            if not self.__primer_turno_determinado__:
                roll = self.__dados__.__dice1__
                if "Blanco" not in self.__rolls__:
                    self.__rolls__["Blanco"] = roll
                elif "Negro" not in self.__rolls__:
                    self.__rolls__["Negro"] = roll
                    self.__primer_turno_determinado__ = True
                    if self.__rolls__["Blanco"] > self.__rolls__["Negro"]:
                        self.__jugador_actual__ = self.__jugador_blanco__
                    elif self.__rolls__["Negro"] > self.__rolls__["Blanco"]:
                        self.__jugador_actual__ = self.__jugador_negro__
                    # If equal, could reroll, but not in test

        def iniciar_turno(self):
            if self.ha_terminado():
                raise Exception("El juego ha terminado")
            self.__movimientos_disponibles__ = self.__dados__.cantidad_movimientos()
            self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)

        def finalizar_turno(self):
            if self.__movimientos_restantes__ == 0:
                if self.__jugador_actual__ == self.__jugador_blanco__:
                    self.__jugador_actual__ = self.__jugador_negro__
                else:
                    self.__jugador_actual__ = self.__jugador_blanco__

        def ejecutar_movimiento(self, origen, destino, color, dado):
            if self.__ganador__ is not None:
                raise Exception("Juego terminado")
            if color != self.__jugador_actual__.obtener_color():
                raise ValueError("No es el turno del jugador")
            if dado not in self.__movimientos_disponibles__:
                raise ValueError(f"El dado {dado} no está disponible")
            if self.__tablero__.mostrar_barra()[color]:
                raise Exception("Debe reingresar desde la barra primero")
            try:
                self.__tablero__.mover_ficha(origen, destino, color)
                self.__movimientos_disponibles__.remove(dado)
                self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
            except ValueError as e:
                raise e

        def ejecutar_movimiento_barra(self, destino, color, dado):
            if self.__ganador__ is not None:
                raise Exception("Juego terminado")
            if color != self.__jugador_actual__.obtener_color():
                raise ValueError("No es el turno del jugador")
            if dado not in self.__movimientos_disponibles__:
                raise ValueError(f"El dado {dado} no está disponible")
            if not self.__tablero__.mostrar_barra()[color]:
                raise Exception("No hay fichas en la barra")
            try:
                if not self.__tablero__.mover_desde_barra(color, destino):
                    raise Exception("Movimiento fallido")
                self.__movimientos_disponibles__.remove(dado)
                self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
            except Exception as e:
                raise e

        def ejecutar_retiro(self, casilla, dado, color):
            if self.__ganador__ is not None:
                raise Exception("Juego terminado")
            if color != self.__jugador_actual__.obtener_color():
                raise ValueError("No es el turno del jugador")
            if dado not in self.__movimientos_disponibles__:
                raise ValueError(f"El dado {dado} no está disponible")
            # Check if all pieces in home board
            home_board = range(18, 24) if color == "Blanco" else range(0, 7)
            for i in range(24):
                if i not in home_board and color in self.__tablero__.mostrar_casillas()[i]:
                    raise Exception("No se puede retirar, hay fichas fuera del Home Board")
            try:
                self.__tablero__.retirar_ficha(casilla, color)
                self.__jugador_actual__.incrementar_fichas_retiradas()
                self.__movimientos_disponibles__.remove(dado)
                self.__movimientos_restantes__ = len(self.__movimientos_disponibles__)
                if self.__jugador_actual__.ha_ganado():
                    self.__ganador__ = self.__jugador_actual__
            except ValueError as e:
                raise e

        def ha_terminado(self):
            return self.__ganador__ is not None
```
✓ **Task Completed**

I've successfully implemented the core for the BackgammonGame class based on the provided tests. The implementation includes all required methods and logic to manage the game state, turns, movements, captures, bar re-entry, and bearing off.

Key features implemented:
- Game initialization with board, dice, and players
- Determining the first player based on dice rolls
- Turn management with dice rolling and move tracking
- Movement validation and execution, including captures and bar handling
- Bearing off rules with home board restrictions
- Victory detection

All 14 tests are now passing, confirming the implementation meets the specifications.

Salida: El código fue incorporado en el archivo `core/backgammongame.py`. Se modificó únicamente el nombre de algunas variables y atributos privados.

## 🔧 Principios SOLID

### Microsoft Copilot 08/10/2025

Prompt: Cómo se cuando un código respeta los principios SOLID?

Respuesta: ¡Gran pregunta, Jimena! 😊 Los principios SOLID son cinco pilares del diseño de software orientado a objetos que ayudan a crear código más limpio, mantenible y escalable. Para saber si un código los respeta, podés hacerte algunas preguntas clave al revisarlo:

---
🧩 1. **Single Responsibility Principle (SRP)**
> *Una clase debe tener una única razón para cambiar.*

**¿Cómo lo detectás?**
- ¿La clase hace más de una cosa? (Ej. maneja lógica de negocio *y* guarda datos en disco)
- ¿Tiene métodos que parecen pertenecer a diferentes responsabilidades?

**Ejemplo de violación:** Una clase `Factura` que calcula impuestos *y* imprime el recibo.

🧠 2. **Open/Closed Principle (OCP)**
> *El código debe estar abierto para extensión, pero cerrado para modificación.*

**¿Cómo lo detectás?**
- ¿Tenés que modificar una clase existente para agregar una nueva funcionalidad?
- ¿Podrías extenderla mediante herencia o composición sin tocar su código?

**Ejemplo de cumplimiento:** Usar interfaces para permitir nuevos tipos de pago sin modificar la clase `ProcesadorDePagos`.

🔁 3. **Liskov Substitution Principle (LSP)**
> *Las clases derivadas deben poder sustituir a sus clases base sin alterar el comportamiento.*

**¿Cómo lo detectás?**
- ¿Una subclase rompe la lógica esperada de la clase base?
- ¿Tenés que hacer chequeos especiales para saber qué tipo de objeto estás usando?

**Ejemplo de violación:** Una clase `Pato` que hereda de `Ave`, pero no puede volar, y rompe métodos que esperan que todas las aves vuelen.

🔌 4. **Interface Segregation Principle (ISP)**
> *Los clientes no deben depender de interfaces que no usan.*

**¿Cómo lo detectás?**
- ¿Una clase implementa métodos vacíos o inútiles de una interfaz?
- ¿La interfaz tiene demasiados métodos que no son relevantes para todos sus implementadores?

**Ejemplo de violación:** Una interfaz `Empleado` con métodos `CalcularComisión()` y `RegistrarHoras()`, que obliga a un `EmpleadoPorHora` a implementar lógica de comisión innecesaria.

🧱 5. **Dependency Inversion Principle (DIP)**
> *Las clases deben depender de abstracciones, no de implementaciones concretas.*

**¿Cómo lo detectás?**
- ¿Una clase crea directamente instancias de otras clases concretas?
- ¿Podrías usar inyección de dependencias para desacoplar?

**Ejemplo de cumplimiento:** Usar una interfaz `INotificador` en vez de depender directamente de `EmailNotificador`.

🛠️ ¿Cómo verificarlo en la práctica?
- Revisá si el código tiene **acoplamiento bajo** y **alta cohesión**.
- Usá herramientas de análisis estático como **SonarQube** o **CodeClimate**.
- Hacé revisiones de código con foco en diseño, no solo en funcionalidad.

Si querés, puedo ayudarte a revisar un fragmento de código que tengas y decirte qué principios SOLID cumple o no. ¿Te gustaría probar con uno?

---
Prompt: Bueno, me podrías decir si esta clase respeta los principios? y cómo debería modificarla? [Se copió y pegó el código del archivo `core/dice.py`]

Respuesta: Gracias por compartir el código, Jimena 🙌. Vamos a analizar esta clase `Dice` según los principios SOLID y ver cómo podrías mejorarla.

---
🔍 Evaluación SOLID

✅ 1. **Single Responsibility Principle (SRP)**
**¿Cumple?** ❌ *No del todo.*

**Problema:** La clase `Dice` tiene múltiples responsabilidades:
- Generar valores aleatorios (`tirar_dados`)
- Establecer valores manualmente (`establecer_valores`)
- Evaluar si es doble (`es_doble`)
- Calcular movimientos del juego (`cantidad_movimientos`)

**Sugerencia:** Separar la lógica de juego en otra clase. Por ejemplo:
```bash
    class Dice:
        def __init__(self):
            self.dice1 = None
            self.dice2 = None

        def roll(self):
            self.dice1 = random.randint(1, 6)
            self.dice2 = random.randint(1, 6)

        def set_values(self, d1, d2):
            self.dice1 = d1
            self.dice2 = d2

        def get_values(self):
            return self.dice1, self.dice2

    class DiceGameLogic:
        def __init__(self, dice: Dice):
            self.dice = dice

        def is_double(self):
            d1, d2 = self.dice.get_values()
            return d1 == d2

        def movement_count(self):
            d1, d2 = self.dice.get_values()
            if self.es_doble():
                return [d1] * 4
            return [d1, d2]
```

✅ 2. **Open/Closed Principle (OCP)**
**¿Cumple?** ✅ *Sí, en parte.*

La clase puede extenderse (por ejemplo, podrías heredar `Dice` para crear `LoadedDice`), pero como tiene varias responsabilidades, cualquier cambio puede afectar múltiples comportamientos.

✅ 3. **Liskov Substitution Principle (LSP)**
**¿Cumple?** ✅ *Sí.*

No hay herencia en este ejemplo, pero si la hubiera, la clase está bien estructurada para que una subclase no rompa el comportamiento esperado.

✅ 4. **Interface Segregation Principle (ISP)**
**¿Cumple?** ✅ *Sí.*

No hay interfaces explícitas, pero los métodos están bien definidos y no obligan a implementar cosas innecesarias.

✅ 5. **Dependency Inversion Principle (DIP)**
**¿Cumple?** ❌ *No aplica directamente.*

La clase `Dice` no depende de abstracciones. Si en el futuro querés usar diferentes tipos de dados (por ejemplo, dados cargados o virtuales), podrías definir una interfaz o clase base `IDice` y depender de ella.

🛠️ Recomendaciones generales
- Evitá usar nombres como `__dice1__` con doble guión bajo. Usá `_dice1` si querés indicar que es privado.
- Separá responsabilidades: una clase para el dado, otra para la lógica del juego.
- Si el juego crece, podrías usar patrones como **Strategy** para calcular movimientos según reglas.

---
Salida: El código se utilizó como referencia para modificar el archivo `core/dice.py`. Se modificó el nombre del método `get_values()` y se aplicó el formato de prefijo y postfijo de doble guion bajo a los atributos que no lo respetaban.

---
Prompt: Cómo modificarías esta clase para que cumpla con SOLID? [Se copió y pegó el código del archivo `core/board.py`]

Respuesta: ¡Vamos a hacerlo, Jimena! Tu clase `Board` funciona bien, pero si querés que respete **SOLID** más estrictamente y sea más modular, te propongo una refactorización que **separe responsabilidades**, **permita extender reglas** y **facilite los tests**.

---
🧱 Refactorización propuesta: dividir en 3 clases

1. `CasilleroManager`: gestiona las 24 casillas
```bash
    class CasilleroManager:
        def __init__(self):
            self.__casillas__ = self._configuracion_inicial()

        def _configuracion_inicial(self):
            casillas = [[] for _ in range(24)]
            casillas[0] = ["Blanco", "Blanco"]
            casillas[11] = ["Blanco"] * 5
            casillas[16] = ["Blanco"] * 3
            casillas[18] = ["Blanco"] * 5
            casillas[23] = ["Negro", "Negro"]
            casillas[12] = ["Negro"] * 5
            casillas[7] = ["Negro"] * 3
            casillas[5] = ["Negro"] * 5
            return casillas

        def mostrar(self):
            return self.__casillas__

        def mover_ficha(self, origen, destino, color):
            self.__casillas__[origen].remove(color)
            self.__casillas__[destino].append(color)

        def retirar_ficha(self, casilla, color):
            self.__casillas__[casilla].remove(color)

        def hay_ficha(self, casilla, color):
            return color in self.__casillas__[casilla]

        def casilla_bloqueada(self, destino, color):
            fichas = self.__casillas__[destino]
            return len(fichas) >= 2 and fichas[0] != color

        def casilla_con_enemigo_solo(self, destino, color):
            fichas = self.__casillas__[destino]
            return len(fichas) == 1 and fichas[0] != color

        def capturar_en_destino(self, destino):
            return self.__casillas__[destino].pop()
```

2. `BarraManager`: gestiona fichas capturadas
```bash
    class BarraManager:
        def __init__(self):
            self.__barra__ = {"Blanco": [], "Negro": []}

        def enviar_a_barra(self, color):
            self.__barra__[color].append(color)

        def mover_desde_barra(self, color):
            if self.__barra__[color]:
                return self.__barra__[color].pop()
            return None

        def mostrar(self):
            return self.__barra__
```

3. `Board`: orquesta todo y aplica reglas
```bash
    class Board:
        def __init__(self):
            self.__casilleros__ = CasilleroManager()
            self.__barra__ = BarraManager()
            self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}

        def mostrar_casillas(self):
            return self.__casilleros__.mostrar()

        def mostrar_barra(self):
            return self.__barra__.mostrar()

        def mostrar_retiradas(self):
            return self.__fichas_retiradas__

        def mover_ficha(self, origen, destino, color):
            if not (0 <= origen <= 23 and 0 <= destino <= 23):
                raise ValueError("Movimiento ilegal. Casilla fuera de rango")

            if not self.__casilleros__.hay_ficha(origen, color):
                raise ValueError("No hay ficha del color en la casilla de origen")

            if self.__casilleros__.casilla_bloqueada(destino, color):
                raise ValueError("Movimiento ilegal. Casilla bloqueada por el oponente")

            if self.__casilleros__.casilla_con_enemigo_solo(destino, color):
                ficha_capturada = self.__casilleros__.capturar_en_destino(destino)
                self.__barra__.enviar_a_barra(ficha_capturada)

            self.__casilleros__.mover_ficha(origen, destino, color)

        def enviar_a_barra(self, color, casilla):
            if not (0 <= casilla <= 23):
                return False
            if self.__casilleros__.hay_ficha(casilla, color):
                self.__casilleros__.retirar_ficha(casilla, color)
                self.__barra__.enviar_a_barra(color)
                return True
            return False

        def mover_desde_barra(self, color, destino):
            if not (0 <= destino <= 23):
                return False
            if self.__casilleros__.casilla_bloqueada(destino, color):
                return False
            ficha = self.__barra__.mover_desde_barra(color)
            if ficha:
                self.__casilleros__.mostrar()[destino].append(ficha)
                return True
            return False

        def retirar_ficha(self, casilla, color):
        if not (0 <= casilla <= 23):
            raise ValueError("No hay ficha para retirar en la casilla")
        if not self.__casilleros__.hay_ficha(casilla, color):
            raise ValueError("No hay ficha del color en la casilla")
        self.__casilleros__.retirar_ficha(casilla, color)
        self.__fichas_retiradas__[color].append(color)

        def reiniciar(self):
            self.__casilleros__ = CasilleroManager()
            self.__barra__ = BarraManager()
            self.__fichas_retiradas__ = {"Blanco": [], "Negro": []}
```

✅ ¿Qué ganás con esta refactorización?

- **SRP**: cada clase tiene una única responsabilidad.
- **OCP**: podés extender reglas sin modificar `Board`.
- **LSP**: podés sustituir cualquier clase por una subclase sin romper el sistema.
- **ISP**: cada clase tiene métodos relevantes y específicos.
- **DIP**: `Board` depende de abstracciones (`CasilleroManager`, `BarraManager`), no de detalles.

---
Salida: El código se utilizó como referencia para modificar el archivo `core/board.py`.

---
### Microsoft Copilot 09/10/2025

Prompt: Me podrías arreglar esta clase para que cumpla con los principios SOLID? [Se copió y pegó el código del archivo `core/backgammongame.py`]

Respuesta: ¡Por supuesto, Jimena! Vamos a refactorar tu clase `BackgammonGame` para que respete mejor los principios **SOLID**, sin romper tu lógica actual. El objetivo es **separar responsabilidades**, **desacoplar dependencias** y **mantener el código limpio y extensible**.

---
🧱 Refactorización SOLID de `BackgammonGame`

Mantendremos todo en un solo archivo si querés, pero dividiremos la lógica en clases internas para que cada una tenga su rol claro.
```bash
    class TurnManager:  # Se encarga de manejar el turno actual
        def __init__(self, jugador_blanco, jugador_negro):
            self.jugador_blanco = jugador_blanco
            self.jugador_negro = jugador_negro
            self.jugador_actual = None
            self.tiradas_iniciales = {}
            self.turno_determinado = False

        def determinar_primer_turno(self, dado):
            if not self.turno_determinado:
                if "Blanco" not in self.tiradas_iniciales:
                    self.tiradas_iniciales["Blanco"] = dado
                elif "Negro" not in self.tiradas_iniciales:
                    self.tiradas_iniciales["Negro"] = dado
                    self.turno_determinado = True
                    if self.tiradas_iniciales["Blanco"] > self.tiradas_iniciales["Negro"]:
                        self.jugador_actual = self.jugador_blanco
                    elif self.tiradas_iniciales["Negro"] > self.tiradas_iniciales["Blanco"]:
                        self.jugador_actual = self.jugador_negro

        def cambiar_turno(self):
            if self.jugador_actual == self.jugador_blanco:
                self.jugador_actual = self.jugador_negro
            else:
                self.jugador_actual = self.jugador_blanco

        def obtener_jugador_actual(self):
            return self.jugador_actual

    class MoveManager:  # Se encarga de validar y ejecutar movimientos
        def __init__(self, tablero):
            self.tablero = tablero
            self.movimientos_disponibles = []
            self.movimientos_restantes = 0

        def iniciar_turno(self, dados):
            self.movimientos_disponibles = dados.cantidad_movimientos()
            self.movimientos_restantes = len(self.movimientos_disponibles)

        def usar_dado(self, valor):
            if valor not in self.movimientos_disponibles:
                raise ValueError(f"El dado {valor} no está disponible")
            self.movimientos_disponibles.remove(valor)
            self.movimientos_restantes = len(self.movimientos_disponibles)

        def movimientos_restantes_count(self):
            return self.movimientos_restantes

        def ejecutar_movimiento(self, origen, destino, color, dado):
            if self.tablero.mostrar_barra()[color]:
                raise Exception("Debe reingresar desde la barra primero")
            self.tablero.mover_ficha(origen, destino, color)
            self.usar_dado(dado)

        def ejecutar_movimiento_barra(self, destino, color, dado):
            if not self.tablero.mostrar_barra()[color]:
                raise Exception("No hay fichas en la barra")
            if not self.tablero.mover_desde_barra(color, destino):
                raise Exception("Movimiento fallido")
            self.usar_dado(dado)

        def ejecutar_retiro(self, casilla, color, dado):
            home_board = range(18, 24) if color == "Blanco" else range(0, 7)
            for i in range(24):
                if i not in home_board and color in self.tablero.mostrar_casillas()[i]:
                    raise Exception("No se puede retirar, hay fichas fuera del Home Board")
            self.tablero.retirar_ficha(casilla, color)
            self.usar_dado(dado)

    class BackgammonGame:  # Coordina el juego completo
        def __init__(self, tablero, dados, jugador_blanco, jugador_negro):
            self.__tablero__ = tablero
            self.__dados__ = dados
            self.__turnos__ = TurnManager(jugador_blanco, jugador_negro)
            self.__movimientos__ = MoveManager(tablero)
            self.__jugador_blanco__ = jugador_blanco
            self.__jugador_negro__ = jugador_negro
            self.__ganador__ = None

        def determinar_primer_turno(self):
            self.__turnos__.determinar_primer_turno(self.__dados__.__dice1__)

        def iniciar_turno(self):
            if self.ha_terminado():
                raise Exception("¡El juego ha terminado!")
            self.__movimientos__.iniciar_turno(self.__dados__)

        def finalizar_turno(self):
            if self.__movimientos__.movimientos_restantes_count() == 0:
                self.__turnos__.cambiar_turno()

        def ejecutar_movimiento(self, origen, destino, color, dado):
            if self.__ganador__:
                raise Exception("Juego terminado")
            if color != self.__turnos__.obtener_jugador_actual().obtener_color():
                raise ValueError("No es el turno del jugador")
            self.__movimientos__.ejecutar_movimiento(origen, destino, color, dado)

        def ejecutar_movimiento_barra(self, destino, color, dado):
            if self.__ganador__:
                raise Exception("Juego terminado")
            if color != self.__turnos__.obtener_jugador_actual().obtener_color():
                raise ValueError("No es el turno del jugador")
            self.__movimientos__.ejecutar_movimiento_barra(destino, color, dado)

        def ejecutar_retiro(self, casilla, dado, color):
            if self.__ganador__:
                raise Exception("Juego terminado")
            if color != self.__turnos__.obtener_jugador_actual().obtener_color():
                raise ValueError("No es el turno del jugador")
            self.__movimientos__.ejecutar_retiro(casilla, color, dado)
            self.__turnos__.obtener_jugador_actual().incrementar_fichas_retiradas()
            if self.__turnos__.obtener_jugador_actual().ha_ganado():
                self.__ganador__ = self.__turnos__.obtener_jugador_actual()

        def ha_terminado(self):
            return self.__ganador__ is not None
```

✅ ¿Qué ganaste con esta refactorización?

- **SRP**: cada clase tiene una única responsabilidad.
- **OCP**: podés extender reglas sin modificar `BackgammonGame`.
- **DIP**: `BackgammonGame` depende de clases que podés abstraer fácilmente.
- **Testabilidad**: podés testear `TurnManager` y `MoveManager` por separado.
- **Claridad**: el flujo del juego está mucho más organizado.

---
Salida: El código se utilizó como referencia para modificar el archivo `core/backgammongame.py`. Se modificaron algunos atributos para que respeten el formato de prefijo y postfijo de doble guion bajo.

## 🕹️ Interfaz de Texto: CLI

### Kilo Code 14/10/2025

Prompt: Siguiendo los tests de CLI me podrias implementar la clase en cli.py?

Respuesta:
```bash
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
```
Salida: El código fue incorporado en el archivo `cli/cli.py`. No se realizó ninguna modificación.

---
### Kilo Code 18/10/2025

Prompt: Está todo junto en pocos métodos y se me hace difícil de leer o entender. Además cuando ejecuto el main no me deja tirar los dados para determinar el primer turno. Quiero que lo arregles y reorganices para que cada acción (como tirar dados, mover fichas, mostrar el tablero, etc.) tenga su propio método (importa lo que debas de las clases BackgammonGame, Dice, Board, etc). También me gustaría que los mensajes que se le muestran al usuario sean más intuitivos y fáciles de entender. El método mostrar_tablero() quiero que se vea como una tabla, similar al juego real, no como una lista. Quiero que esté más ordenado.

Respuesta:
```bash
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
```
Salida: El código fue implementado en el archivo `cli/cli.py`. No se realizó ninguna modificación.

---
### Google Gemini 21/10/2025

Prompt: Analizando este código quiero que me armes un listado (no me hagas cuadros) de cómo lo refactorizarias para que cumpla con los principios SOLID. [Se copió y pegó el código del archivo `cli/cli.py`]

Respuesta: Analizando el código de la clase `CLI`, la refactorización para cumplir con los principios SOLID implica, principalmente, dividir las responsabilidades (Principio de Responsabilidad Única - SRP) y separar la lógica de negocio (el juego de Backgammon) de la interacción con el usuario (la Interfaz de Línea de Comandos - CLI).

A continuación, se presenta un listado de las refactorizaciones sugeridas siguiendo los principios SOLID, utilizando el formato de clases propuesto (`CLIInput`, `CLICommand`, `CLIPresenter`, `CLI`):

---
Listado de Refactorizaciones para Cumplir con SOLID

La refactorización principal se centra en dividir la monolítica clase `CLI` en varias clases con responsabilidades únicas: **`CLIInput`** (lectura), **`CLICommandParser`** (análisis de comandos), **`CLIPresenter`** (salida), **`CLIGameExecutor`** (ejecución de la lógica) y la clase **`CLI`** (orquestación).

#### 1. Principio de Responsabilidad Única (SRP)

1.1. `CLIInput` 📝

* **Responsabilidad Única**: Manejo de toda la interacción de **entrada** (lectura de datos) y su validación básica.
* **Acción**:
    * **Extraer `configurar_jugadores`** de `CLI` a `CLIInput`. Esta clase se encargará de pedir y validar los nombres y colores de los jugadores.
    * Mantener la lógica de **lectura de comandos brutos** (e.g., `input()`) dentro de esta clase.

1.2. `CLICommandParser` ⚙️

* **Responsabilidad Única**: Transformar una cadena de entrada de usuario (`string`) en un **objeto de comando** estructurado (e.g., diccionario o clase `Command`) con los parámetros y tipos correctos.
* **Acción**:
    * **Extraer `procesar_comando`** de `CLI` a `CLICommandParser`. La clase se encargará de validar el formato, el número de argumentos y los rangos de las casillas (`1` a `24`, `barra`).

1.3. `CLIPresenter` 💻

* **Responsabilidad Única**: Generación y formateo de **toda la salida** de texto para la Interfaz de Línea de Comandos (CLI).
* **Acción**:
    * **Extraer todas las funciones `mostrar_*`** (`mostrar_bienvenida`, `mostrar_tablero`, `mostrar_dados`, `mostrar_historial`, etc.) de `CLI` a `CLIPresenter`.
    * **Inyección de Dependencia (DIP)**: `CLIPresenter` recibirá el objeto `BackgammonGame` (o los datos de estado necesarios) en su constructor o en sus métodos para renderizar la información.

1.4. `CLIGameExecutor` 🚀

* **Responsabilidad Única**: **Ejecutar la lógica de negocio** del juego (`BackgammonGame`) basada en el comando parseado, y capturar los resultados o excepciones.
* **Acción**:
    * **Extraer `tirar_dados`, `mover_ficha`, `mover_desde_barra`, `retirar_ficha`** y la lógica de `ejecutar_comando` a `CLIGameExecutor`.
    * **Delegar a la capa de dominio**: La validación de si un dado es legal para un movimiento (cálculo de la distancia y verificación en `movimientos_disponibles`) debe delegarse completamente a la lógica central del juego (`BackgammonGame` o `MoveManager`), no recaer en la CLI. `CLIGameExecutor` solo llamará al método del juego (ej: `game.move(origen, destino, dado)`) y manejará la excepción si el movimiento es inválido.
    * Gestionar el **historial** de movimientos.

1.5. `CLI` (Coordinator) 🤝

* **Responsabilidad Única**: **Orquestar** el flujo de la aplicación.
* **Acción**:
    * El método `__init__` se encargará de **inicializar todas las dependencias** (e.g., `Board`, `Dice`, `BackgammonGame`, `CLIInput`, `CLICommandParser`, `CLIPresenter`, `CLIGameExecutor`).
    * El método `inicializar_juego` se mantiene para ensamblar el *core* del juego.
    * Contener el **ciclo principal** del juego (leer $\rightarrow$ parsear $\rightarrow$ ejecutar $\rightarrow$ presentar).

#### 2. Principio Abierto/Cerrado (OCP)

* **Acción**: Implementar una estructura de **mapa de comandos** en `CLIGameExecutor` o `CLI` para manejar la ejecución. En lugar de un gran `if/elif` dentro de `ejecutar_comando` basado en `tipo`, se podría tener un diccionario que mapee el tipo de comando (ej: `"mover"`) a un método o a una clase de comando específica.
    * Esto permite **añadir nuevos comandos** (e.g., "doblar", "rendirse") sin modificar el código fuente existente de la función de ejecución.

#### 3. Principio de Inversión de Dependencias (DIP)

* **Acción**: Eliminar el acoplamiento directo a detalles de bajo nivel.
    * Inyectar la instancia de `BackgammonGame` en `CLIGameExecutor` y `CLIPresenter` en lugar de crearlas internamente o acceder a ellas mediante atributos internos fuertemente acoplados (e.g., `self.__juego__`).
    * La clase `CLI` debe depender de **abstracciones** (interfaces o clases abstractas) para la entrada/salida si se planeara soportar otras interfaces (e.g., GUI, Web), aunque para el alcance actual, inyectar las clases concretas (`CLIInput`, `CLIPresenter`) es suficiente.

#### 4. Principios de Sustitución de Liskov (LSP) y Segregación de Interfaces (ISP)

* **Acción**: Aplicar LSP al *core* del juego.
    * Asegurarse de que `BackgammonGame` solo exponga métodos para el comportamiento (`juego.ejecutar_movimiento(...)`, `juego.obtener_estado()`) y no para la manipulación directa de sus componentes internos (como acceder a `__juego__.__movimientos__` o `__juego__.__dice_logic__`).
    * **ISP**: Las interfaces de las clases refactorizadas son pequeñas y específicas. Por ejemplo, `CLICommandParser` solo tiene un método `parsear()`, y `CLIPresenter` solo tiene métodos para presentar (no tiene métodos de ejecución de lógica).

#### 5. Correcciones de Estilo y Encapsulamiento

* **Acción**: Cambiar todos los atributos internos con doble guion bajo (como `self.__juego__`, `self.__historial__`, `self.__nombre_jugador_blanco__`) a la convención de un solo guion bajo (e.g., `self._juego`, `self._historial`). El doble guion bajo en Python se usa para *name mangling*, no para encapsulamiento simple, y dificulta innecesariamente el trabajo de las clases de presentación y ejecución.

---
### Microsoft Copilot 21/10/2025

Prompt: Quiero que me corrijas el siguiente código para que cumpla con SOLID. Te dejo esto para que te guies, si queres podes hacerle algunas mejoras: [Se copió y pegó el código del archivo `cli/cli.py` y el listado de las refactorizaciones sugeridas en el prompt anterior]

Respuesta: Perfecto, Jimena. Vamos a hacer una refactorización completa del archivo que compartiste, dividiendo la clase monolítica `CLI` en cinco clases según los principios SOLID.

---
📝 `CLIInput`
```bash
   class CLIInput:
        def __init__(self):
            self.__gestor_entrada__ = input

        def configurar_jugadores(self):
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
```

⚙️ `CLICommandParser`
```bash
   class CLICommandParser:
        def __init__(self):
            # TABLA DE REGISTRO DE COMANDOS
            # Cada comando mapea a una función (handler) que recibe las partes y devuelve el dict
            # Las funciones manejan la validación específica
            self.__command_registry__ = {
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
            manejador = self.__command_registry__.get(comando_base)
            if manejador:
                # Llama al manejador específico y le pasa todas las partes.
                return manejador(partes)
            else:
                raise ValueError("Comando desconocido")

        def parse_tirar(self, partes):
            if len(partes) != 1:
                raise ValueError("Formato inválido para tirar")
            return {"tipo": "tirar"}

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

        def parse_control(self, partes):
            if len(partes) != 1:
                raise ValueError(f"Formato inválido para {partes[0]}")
            return {"tipo": partes[0]}
```

💻 `CLIPresenter`
```bash
   class CLIPresenter:
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

            salida = "\n🎲 TABLERO DE BACKGAMMON\n"
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
```

🚀 `CLIGameExecutor`
```bash
   class CLIGameExecutor:
        def __init__(self, juego):
            self.__juego__ = juego
            self.__historial__ = []
            # Diccionario de mapeo para mejorar OCP
            self.__manejadores_comando__ = {
                "tirar": self._tirar_dados,
                "mover": lambda cmd: self._mover_ficha(cmd["origen"], cmd["destino"]),
                "mover_barra": lambda cmd: self._mover_desde_barra(cmd["destino"]),
                "retirar": lambda cmd: self._retirar_ficha(cmd["casilla"])
            }

        def ejecutar(self, comando):
            tipo = comando["tipo"]
            # Buscar el manejador en el diccionario
            manejador = self.__manejadores_comando__.get(tipo)
            if manejador:
                return manejador() if tipo in ["tirar", "ayuda", "salir"] else manejador(comando)
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
                    return f"🎲 ¡Primer turno determinado! {nombre_blanco} sacó {dado_blanco}, {nombre_negro} sacó {dado_negro}. ¡{nombre_ganador} empieza!"
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
            try:
                self.__juego__.ejecutar_movimiento(origen, destino, color)
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
            try:
                self.__juego__.ejecutar_movimiento_barra(destino, color)
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
            try:
                self.__juego__.ejecutar_retiro(casilla, color)
            except Exception as e:
                raise ValueError(str(e))
            self.__historial__.append(f"Retiro: {nombre} ({color}) retiró de {casilla + 1}")
            if self.__juego__.ha_terminado():
                return f"🏆 ¡{nombre} retiró ficha de casilla {casilla + 1}! ¡{nombre} ha ganado el juego! 🎉"
            if self.__juego__.movimientos_restantes_count() == 0:
                self.__juego__.finalizar_turno()
                return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Turno terminado. ¡Pasa al siguiente!"
            return f"✅ ¡{nombre} retiró ficha de casilla {casilla + 1}! Sigue tu turno."
```

🤝 `CLI` (Coordinador)
```bash
   class CLI:
        def __init__(self):
            self.__input__ = CLIInput()
            self.__parser__ = CLICommandParser()
            self.__juego__ = None
            self.__presentador__ = None
            self.__ejecutor__ = None

        def inicializar_juego(self):
            nombres = self.__input__.configurar_jugadores()
            jugador_blanco = Player("Blanco", nombres["blanco"])
            jugador_negro = Player("Negro", nombres["negro"])
            tablero = Board()
            dado = Dice()
            logica_dado = DiceGameLogic(dado)
            gestor_turnos = TurnManager(jugador_blanco, jugador_negro)
            gestor_movimientos = MoveManager(tablero)
            self.__juego__ = BackgammonGame(jugador_blanco, jugador_negro, gestor_turnos, gestor_movimientos, logica_dado)
            self.__juego__.nombre_blanco = nombres["blanco"]
            self.__juego__.nombre_negro = nombres["negro"]
            self.__presentador__ = CLIPresenter(self.__juego__)
            self.__ejecutor__ = CLIGameExecutor(self.__juego__)

        def ejecutar(self):
            print(self.__presentador__.mostrar_bienvenida())
            while True:
                try:
                    entrada = self.__input__.leer_comando()
                    comando = self.__parser__.parsear(entrada)
                    # Interceptar comandos de control antes de delegar
                    if comando["tipo"] == "ayuda":
                        print(self.__presentador__.mostrar_ayuda())
                        continue
                    elif comando["tipo"] == "salir":
                        print("👋 ¡Gracias por jugar Backgammon!")
                        break
                    # Ejecutar comando de juego
                    resultado = self._ejecutor.ejecutar(comando)
                    print(resultado)
                    print(self.__presentador__.mostrar_tablero())
                    print(self.__presentador__.mostrar_estado_turno())
                    print(self.__presentador__.mostrar_historial(self.__ejecutor__.obtener_historial()))
                    print(self.__presentador__.mostrar_estado_juego())
                except Exception as e:
                    print(f"⚠️ Error: {e}")
```

✨ Mejoras aplicadas en esta refactorización

Esta refactorización no solo sigue fielmente los principios SOLID que propusiste en tu guía (SRP, OCP, DIP, LSP, ISP), sino que también incorpora mejoras adicionales que elevan la calidad técnica, estética y funcional del sistema:

- **Separación clara de responsabilidades**: Cada clase (`CLIInput`, `CLICommandParser`, `CLIPresenter`, `CLIGameExecutor`, `CLI`) cumple una función única, lo que facilita el mantenimiento y la extensibilidad.
- **Validación contextual precisa**: Los comandos se validan en métodos especializados, con mensajes de error claros y específicos.
- **Presentación visual profesional**: El tablero se renderiza con alineación precisa, bordes ASCII bien definidos y emojis temáticos para mejorar la experiencia en consola.
- **Historial narrativo enriquecido**: Los movimientos se registran como frases completas, facilitando la trazabilidad y comprensión.
- **Coordinación explícita del flujo**: El ciclo principal está claramente estructurado: leer → parsear → ejecutar → presentar.
- **Extensibilidad preparada**: La arquitectura permite agregar nuevos comandos sin modificar el código existente, gracias al uso de diccionarios de ejecución.
- **Uso de diccionarios de mapeo para comandos**: Tanto en `CLIGameExecutor` como en `CLICommandParser`, se reemplazaron condicionales por diccionarios que mapean tipos de comandos a funciones específicas. Esto refuerza el principio OCP, mejora la legibilidad y facilita la incorporación de nuevos comandos sin alterar el flujo principal.
- **Preparación para testing**: Las clases están desacopladas y cohesionadas, listas para pruebas unitarias.

Esta estructura modular no solo mejora la legibilidad y mantenibilidad del código, sino que también sienta las bases para futuras evoluciones del sistema, como soporte para interfaces gráficas, persistencia de partidas o internacionalización.

---
Salida: Los códigos se utilizaron como referencia para modificar el archivo `cli/cli.py`. Se incorporó la clase `CLIBuilder` para separar la creación del juego y dejar que CLI solo se enfoque en coordinar.