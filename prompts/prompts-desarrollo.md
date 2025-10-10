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
---
Si querés, puedo ayudarte a revisar un fragmento de código que tengas y decirte qué principios SOLID cumple o no. ¿Te gustaría probar con uno?

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

---
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
---

✅ ¿Qué ganás con esta refactorización?

- **SRP**: cada clase tiene una única responsabilidad.
- **OCP**: podés extender reglas sin modificar `Board`.
- **LSP**: podés sustituir cualquier clase por una subclase sin romper el sistema.
- **ISP**: cada clase tiene métodos relevantes y específicos.
- **DIP**: `Board` depende de abstracciones (`CasilleroManager`, `BarraManager`), no de detalles.

---
Salida: El código se utilizó como referencia para modificar el archivo `core/board.py`.

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
---

✅ ¿Qué ganaste con esta refactorización?

- **SRP**: cada clase tiene una única responsabilidad.
- **OCP**: podés extender reglas sin modificar `BackgammonGame`.
- **DIP**: `BackgammonGame` depende de clases que podés abstraer fácilmente.
- **Testabilidad**: podés testear `TurnManager` y `MoveManager` por separado.
- **Claridad**: el flujo del juego está mucho más organizado.

---
Salida: El código se utilizó como referencia para modificar el archivo `core/backgammongame.py`. Se modificaron algunos atributos para que respeten el formato de prefijo y postfijo de doble guion bajo.