# Prompts Testing: Registro de IA

## 🎲 Class Dice

### ChatGPT 01/09/2025

Prompt: Que tests se te ocurre que puedo hacer relacionado a los dados del juego backgammon? Tiene que estar relacionado a la lógica de tiradas.

Respuesta: Para los dados de Backgammon, podés cubrir bastante lógica de juego sin salirte de la clase. Te paso ideas de tests que van directo a la mecánica de tiradas:

---
📌 Ideas de tests para los dados
1. **Tirada devuelve valores válidos**  
   - Al lanzar los dados se obtienen exactamente dos enteros en el rango `1–6`.
2. **Detección de doble**  
   - Cuando ambos dados son iguales, el método `es_doble()` debe devolver `True`.
3. **Cantidad de movimientos correcta**  
   - Para valores distintos, `cantidad_movimientos()` debe devolver `[d1, d2]`;  
     para un doble `[d1, d1, d1, d1]`.
4. **Secuencia de tiradas válidas**  
   - Al realizar varias tiradas seguidas, cada resultado siempre es una tupla de dos números `1–6`.
5. **Comportamiento sin tirada previa**  
   - Si se consulta `cantidad_movimientos()` antes de tirar, debería devolver `[]`  
     o lanzar una excepción controlada (lo definís vos).
6. **Dobles consecutivos en turnos distintos**  
   - Simular dos tiradas con dobles diferentes (por ejemplo `3,3` y luego `6,6`) y verificar  
     que en cada caso la lista de movimientos es de cuatro valores idénticos.
7. **Reinicio del dado**  
   - Un método `reiniciar()` debería vaciar los valores y hacer que `cantidad_movimientos()`  
     vuelva a `[]` y `es_doble()` sea `False`.
8. **Tiradas repetidas válidas**  
   - Forzar manualmente varias combinaciones distintas y asegurar que nunca devuelve  
     un valor fuera de rango ni listas vacías tras `tirar_dados()`.
9. **Consumo de movimientos** *(si implementás `usar_tirada(valor)`)*  
    - Llamar a `usar_tirada(3)` debe quitar un `3` de la lista y no permitir volver a usarlo si ya no está.
---
Estos casos cubren tanto la **validación de resultados** como el **flujo típico del juego**: tirar, detectar dobles, contar movimientos, conservar o reiniciar estado y, si querés, consumir tiradas.

---
Prompt: Me podrias hacer los test 1, 2 y 3 utilizando unittest en python?

Respuesta:
   ```bash
   import unittest
   from core.dice import Dice


    class TestDadosBasicos(unittest.TestCase):
        def setUp(self):
            """Se crea un objeto Dice antes de cada prueba."""
            self.dado = Dice()

        def test_tirada_devuelve_valores_validos(self):
            """Cada tirada debe devolver exactamente dos números entre 1 y 6."""
            d1, d2 = self.dado.tirar_dados()
            self.assertIn(d1, range(1, 7))
            self.assertIn(d2, range(1, 7))

        def test_deteccion_de_doble(self):
            """Cuando ambos valores son iguales, es_doble() debe devolver True."""
            self.dado.establecer_valores(4, 4)
            self.assertTrue(self.dado.es_doble())

        def test_cantidad_de_movimientos_correcta(self):
            """Para valores distintos, cantidad_movimientos debe devolver ambos valores."""
            self.dado.establecer_valores(2, 5)
            movimientos = self.dado.cantidad_de_movimientos()
            self.assertEqual(movimientos, [2, 5])

    if __name__ == "__main__":
        unittest.main()
   ```
Salida: El código fue incorporado en el archivo `tests/test_dice.py`. Se modificó el nombre de las funciones y algunas variables, y siguiendo la lógica del mismo código, se incorporó que verifique que cuando se obtiene doble la cantidad de movimientos sea 4.

## ♟️ Class Checker

### ChatGPT 03/09/2025

Prompt: Que tests se te ocurre que puedo hacer relacionado a las fichas del juego backgammon? Tene en cuenta que también estan las clases BackgammonGame (coordina flujo general), Board (representa el tablero y puntos), Player (representa a un jugador) y Dice (lógica de tiradas).

Respuesta: Perfecto 😄, vamos a enfocarnos **solo en tests relacionados a las fichas (`Checker`)**, teniendo en cuenta cómo interactúan con `Player`, `Board` y `BackgammonGame`, pero sin mezclar con la lógica de dados (`Dice`).

---
💡 Ideas de tests para `Checker` (fichas)
1. **Inicialización de la ficha**
   * Verificar que al crear un `Checker` se asignen correctamente:
     * Color del jugador
     * Posición inicial (si aplica)
     * Estado (activo, eliminado, etc., según tu implementación)
2. **Mover ficha dentro de un punto válido**
   * Simular mover una ficha de un punto a otro válido del tablero.
   * Verificar que la posición de la ficha se actualiza correctamente.
   * Verificar que el punto anterior se decrementa y el punto destino se incrementa correctamente.
3. **Captura de ficha (hit)**
   * Testear que cuando una ficha es capturada por el oponente:
     * Se mueve a la barra o área de “fuera del tablero” según tu lógica.
     * Su estado se actualiza correctamente.
4. **Conservación de la ficha al mover**
   * Si el movimiento no es válido (por ejemplo, mover más casillas que permitido), la ficha **no debería moverse**.
5. **Interacción mínima con Player**
   * Comprobar que un `Player` puede “poseer” sus fichas correctamente.
   * Testear que el conteo de fichas de un jugador coincide con la cantidad de `Checker` que tiene en el tablero.
6. **Estado final del juego (parcial)**
   * Aunque `BackgammonGame` coordina el flujo, podés hacer tests unitarios para `Checker` verificando si:
     * Ficha llega al “home” o zona de salida
     * Ficha retirada del tablero se contabiliza correctamente
---
**Tips de implementación:**
* Mantener los tests **unitarios solo en `Checker`**, usando mocks o instancias simples de `Player` y `Board` si hace falta.
* No mezclar con la lógica de tiradas de `Dice`; esos tests irían en otra clase.
---
Si querés, puedo hacer un **mini esquema de código de los tests unitarios de `Checker`**, listo para usar con `unittest` y `coverage`, para que veas cómo implementarlos de manera ordenada.

---
Prompt: Me podrias hacer los tests pero sin que dependan de las clases Player y Board?

Respuesta: ¡Sí, totalmente! 😄 Podemos hacer **tests totalmente unitarios para `Checker`**, sin depender de `Player` ni `Board`.
La idea es **probar solo la lógica interna de la ficha**: atributos, cambios de posición, estado activo/inactivo, y validaciones simples.
   ```bash
   import unittest
   from core.checker import Checker

   class TestChecker(unittest.TestCase):

      def setUp(self):
         # Crear una ficha básica sin jugador ni tablero
         self.ficha = Checker(owner="Blanco", position=1)

      def test_inicializacion_ficha(self):
         self.assertEqual(self.ficha.owner, "Blanco")
         self.assertEqual(self.ficha.position, 1)
         self.assertTrue(self.ficha.is_active)

     def test_mover_ficha_valido(self):
         # Simular movimiento dentro de límites del tablero
         self.ficha.move_to(5)
         self.assertEqual(self.ficha.position, 5)

     def test_mover_ficha_invalido(self):
         # Intentar mover a posición fuera de rango (suponiendo tablero 1-24)
         with self.assertRaises(ValueError):
            self.ficha.move_to(25)
         # La posición original no cambia
         self.assertEqual(self.ficha.position, 1)

      def test_desactivar_ficha(self):
         # Cambiar estado de la ficha
         self.ficha.is_active = False
         self.assertFalse(self.ficha.is_active)

   if __name__ == "__main__":
      unittest.main()
   ```
Salida: El código fue incorporado en el archivo `tests/test_checker.py`. Se modificó nuevamente el nombre de algunas funciones y variables, y en `test_desactivar_ficha()` se incorporó que la posición quede en None si la ficha ya no está en el tablero.

## 👤 Class Player

### ChatGPT 10/09/2025

Prompt: Me podrias decir que tests puedo hacer relacionados a la clase Player en el juego de backgammon?

Respuesta: ¡Claro! La clase **`Player`** en Backgammon representa a cada jugador, así que sus tests deberían enfocarse en lo que **un jugador controla** dentro del juego. Te paso un listado de ideas de tests que podrías implementar:

---
📌 Ideas de tests para `Player`
1. **Inicialización correcta**
   * Verificar que el jugador se crea con su color, nombre o identificador.
   * Chequear que su lista de fichas esté vacía (o inicializada) y que comience en estado válido.
2. **Asignación de fichas**
   * Probar que al asignar fichas al jugador, efectivamente se agregan y se puede consultar cuántas tiene.
   * Verificar que no se dupliquen fichas.
3. **Cantidad de fichas en juego**
   * Si tiene 15 fichas al inicio, asegurarse de que el conteo sea correcto.
   * Probar que al mover o capturar fichas se actualice ese número.
4. **Captura de ficha**
   * Simular que una ficha del jugador es enviada a la barra y comprobar que el jugador tiene al menos una ficha “fuera de juego”.
5. **Reingreso de ficha desde la barra**
   * Dar un valor de dado válido y verificar que una ficha capturada puede volver al tablero.
6. **Todas las fichas fuera (condición de victoria)**
   * Simular que todas las fichas del jugador fueron retiradas del tablero → el jugador debería estar en estado “ganador”.
7. **Turnos del jugador**
   * Verificar que el jugador pueda recibir y almacenar los valores de una tirada de dados.
   * Comprobar que puede usar un valor de dado y que ya no esté disponible después de usarlo.
8. **Validación de movimientos permitidos** *(opcional, si Player tiene esa lógica y no Game/Board)*
   * Testear que, dado un valor de dado, el jugador solo pueda mover fichas a posiciones válidas.
---

📌 **Resumen**:  
Los tests de `Player` deben cubrir principalmente:
* **Identidad** (color, nombre).  
* **Gestión de fichas** (cuántas tiene, cuántas en la barra, cuántas retiradas).  
* **Turnos** (tiradas y consumo de dados).  
* **Condiciones especiales** (ganar la partida al retirar todas las fichas).  

---
Prompt: Y con esos tests estas respetando esto? BackgammonGame → Coordina flujo general, Board → Representa el tablero y puntos, Player → Representa a un jugador, Dice → Lógica de tiradas, Checker → Representa cada ficha. O sea, no me estas mezclando las responsabilidades?

Respuesta: Muy buena observación 👌, porque justo ahí está el riesgo: si no separamos bien responsabilidades, los tests de `Player` terminan probando cosas que en realidad pertenecen a `Board` o `BackgammonGame`.

---
📌 Lo que **sí** le corresponde a `Player`
* Identidad del jugador (**color**, nombre, id).
* La **colección de fichas** que le pertenecen (sus 15 checkers).
* Estado general del jugador (ej: sigue en partida, ya ganó, etc.).
* Posiblemente un “contador” de fichas retiradas del tablero (para saber cuándo gana).
---
📌 Lo que **NO** debería hacer `Player`
* **Decidir movimientos** (eso lo hace `BackgammonGame`, usando el `Board` y los `Dice`).
* **Verificar posiciones válidas** (es lógica del `Board`).
* **Aplicar tiradas de dados** directamente (eso es del `Game`, que reparte las tiradas a los jugadores).

---
✅ Entonces, si ajustamos la lista de tests para no mezclar:
1. **Inicialización correcta**
   * Ver que al crear un `Player` sus atributos (`__color__`, nombre, etc.) estén bien.
2. **Asignación de fichas propias**
   * Chequear que se le puedan asociar fichas (`Checker`) y que pertenezcan al jugador.
3. **Cantidad de fichas total**
   * Confirmar que arranca con 15 fichas y que se puede consultar cuántas tiene activas o retiradas.
4. **Marcado de fichas retiradas**
   * Probar que si se incrementa su contador de fichas retiradas, refleje el cambio.
5. **Condición de victoria**
   * Simular que retiró todas las fichas y verificar que el jugador es declarado “ganador”.
---
⚠️ Cosas como “usar tirada de dados” o “mover ficha de posición” no van en `Player`, porque ahí mezclarías con `Dice` o `Board`.

---
Prompt: Bien, entonces me podrías hacer los tests de forma unitaria con unittest? Sin depender de una clase distinta a Player.

Respuesta: ¡Perfecto! Si querés que los tests de **`Player`** sean **unitarios de verdad**, entonces no deben depender de otras clases como `Checker`. Solo testeamos el propio comportamiento de `Player`.
   ```bash
   import unittest
   from core.player import Player


   class TestPlayer(unittest.TestCase):

      def setUp(self):
         # Se crea un jugador antes de cada test
         self.player = Player(color="Negro", nombre="Jugador 1")

      def test_inicializacion(self):
         """El jugador debe crearse con color, nombre y sin fichas."""
         self.assertEqual(self.player.__color__, "Negro")
         self.assertEqual(self.player.__nombre__, "Jugador 1")
         self.assertEqual(self.player.__fichas__, [])
         self.assertEqual(self.player.__fichas_retiradas__, 0)

      def test_agregar_ficha(self):
         """Al agregar una ficha (mock), debe guardarse en la lista."""
         self.player.agregar_ficha("ficha_mock")
         self.assertIn("ficha_mock", self.player.__fichas__)
         self.assertEqual(len(self.player.__fichas__), 1)

      def test_contar_fichas(self):
         """El método contar_fichas debe devolver la cantidad correcta."""
         self.player.__fichas__ = ["f1", "f2", "f3"]
         self.assertEqual(self.player.contar_fichas(), 3)

      def test_incrementar_fichas_retiradas(self):
         """Debe aumentar el contador de fichas retiradas en uno."""
         self.assertEqual(self.player.__fichas_retiradas__, 0)
         self.player.incrementar_fichas_retiradas()
         self.assertEqual(self.player.__fichas_retiradas__, 1)

      def test_condicion_victoria(self):
         """El jugador gana si retiró todas sus fichas (15)."""
         for _ in range(15):
            self.player.incrementar_fichas_retiradas()
         self.assertTrue(self.player.ha_ganado())
         self.assertEqual(self.player.__fichas_retiradas__, 15)

   if __name__ == "__main__":
      unittest.main()
   ```
Salida: El código fue incorporado en el archivo `tests/test_player.py`. Se modificó el nombre de algunas variables y se incorporó los tests para los métodos `obtener_color()` y `obtener_nombre()` de la clase Player.

## 🎯 Class Board

### ChatGPT 15/09/2025

Prompt: Me podrías hacer una lista de tests unitarios específicos para la clase Board siguiendo las reglas reales del juego Backgammon? No quiero tests genéricos.

Respuesta: ¡Muy bien! 👌 Te preparo un listado de ideas de tests unitarios, más alineados con la lógica real del Backgammon, que podrías implementar para tu clase `Board`.

---
📌 Ideas de tests unitarios para `Board`
1. **Inicialización del tablero**
   * Al crear un tablero debe tener 24 casillas.
   * Cada casilla arranca con la disposición inicial estándar de Backgammon (ej. 2 blancas en la casilla 0, 5 negras en la casilla 5, etc.).
   * Barra y retiradas empiezan vacías.
2. **Movimiento de ficha válido**
   * Una ficha puede moverse desde una casilla de origen a otra de destino.
   * El origen pierde una ficha y el destino gana una ficha del color correcto.
3. **Movimiento inválido**
   * Si el origen está vacío, o la ficha no corresponde al color, el movimiento debe lanzar `ValueError`.
   * No se permite mover hacia una casilla ocupada por 2 o más fichas enemigas.
4. **Captura de ficha enemiga**
   * Si el destino tiene exactamente 1 ficha rival, esta debe ser capturada.
   * La ficha capturada desaparece de la casilla y aparece en la **barra** del color contrario.
5. **Enviar ficha a la barra**
   * Se puede forzar el envío de una ficha propia desde una casilla hacia la barra.
   * Si la casilla está vacía o contiene ficha de otro color, no debe hacerlo.
6. **Mover ficha desde la barra**
   * Una ficha que está en la barra puede reingresar al tablero en una casilla válida.
   * Si la barra está vacía o la casilla está bloqueada (2 o más fichas enemigas), el movimiento debe fallar.
7. **Retiro de fichas (retirada/bear off)**
   * Cuando un jugador puede retirarlas, al hacerlo la ficha desaparece de la casilla.
   * La ficha debe quedar registrada en la lista de retiradas del jugador.
   * Si la casilla está vacía o la ficha es de otro color, debe lanzar error.
8. **Reinicio del tablero**
   * El método `reiniciar()` debe restaurar la disposición inicial completa.
   * Barra y retiradas deben volver a estar vacías.
---

📌 **Resumen**  
Los tests de `Board` deben cubrir:
* **Inicialización correcta** (24 casillas con disposición estándar).
* **Operaciones válidas** (mover fichas, capturar, enviar/recuperar de la barra, retirar fichas).
* **Operaciones inválidas** (movimientos ilegales, casillas vacías, colores incorrectos).
* **Estados especiales del juego** (barra, retiradas y reinicio del tablero).

---
Prompt: Bien, me podrías hacer los tests usando unittest en python?

Respuesta:
📂 tests/test_board.py
   ```bash
   import unittest
   from core.board import Board

   class TestBoard(unittest.TestCase):

      def setUp(self):
         self.board = Board()

      # --- Inicialización ---
      def test_inicializacion_casillas(self):
         """El tablero debe iniciar con la configuración estándar de Backgammon."""
         casillas = self.board.mostrar_casillas()
         self.assertEqual(len(casillas), 24)
         self.assertEqual(casillas[0], ["blanco", "blanco"])
         self.assertEqual(casillas[11], ["blanco"] * 5)
         self.assertEqual(casillas[23], ["negro", "negro"])
         self.assertEqual(casillas[5], ["negro"] * 5)

      def test_inicializacion_barra_retiradas_vacias(self):
         """Barra y retiradas deben estar vacías al inicio."""
         self.assertEqual(self.board.mostrar_barra(), {"blanco": [], "negro": []})
         self.assertEqual(self.board.mostrar_retiradas(), {"blanco": [], "negro": []})

      # --- Movimiento de fichas ---
      def test_mover_ficha_valida(self):
         """Mover ficha válido actualiza las casillas."""
         self.board.__casillas__[0] = ["blanco"]
         self.board.__casillas__[1] = []
         self.board.mover_ficha(0, 1, "blanco")
         self.assertIn("blanco", self.board.__casillas__[1])
         self.assertNotIn("blanco", self.board.__casillas__[0])

      def test_mover_ficha_invalida(self):
         """No se puede mover si no es legal."""
         with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "negro")  # no hay negras en 0

      def test_mover_ficha_con_captura(self):
         """Si hay una ficha enemiga sola, debe ir a la barra."""
         self.board.__casillas__[0] = ["blanco"]
         self.board.__casillas__[1] = ["negro"]
         self.board.mover_ficha(0, 1, "blanco")
         self.assertIn("blanco", self.board.__casillas__[1])
         self.assertIn("negro", self.board.__barra__["negro"])

      # --- Barra ---
      def test_enviar_a_barra_valido(self):
         """Enviar ficha a la barra cuando color coincide."""
         self.board.__casillas__[0] = ["blanco"]
         resultado = self.board.enviar_a_barra("blanco", 0)
         self.assertTrue(resultado)
         self.assertIn("blanco", self.board.__barra__["blanco"])
         self.assertEqual(self.board.__casillas__[0], [])

      def test_enviar_a_barra_invalido(self):
         """No debe enviar a barra si casilla vacía o color incorrecto."""
         self.board.__casillas__[0] = []
         self.assertFalse(self.board.enviar_a_barra("blanco", 0))
         self.board.__casillas__[0] = ["negro"]
         self.assertFalse(self.board.enviar_a_barra("blanco", 0))

      def test_mover_desde_barra_valido(self):
         """Mover ficha desde barra a casilla vacía."""
         self.board.__barra__["blanco"].append("blanco")
         resultado = self.board.mover_desde_barra("blanco", 2)
         self.assertTrue(resultado)
         self.assertIn("blanco", self.board.__casillas__[2])
         self.assertEqual(self.board.__barra__["blanco"], [])

      def test_mover_desde_barra_invalido(self):
         """No se mueve desde barra si está vacía."""
         resultado = self.board.mover_desde_barra("negro", 3)
         self.assertFalse(resultado)

      # --- Borne off ---
      def test_bornear_ficha_valida(self):
         """Retirar ficha válida la mueve a retiradas."""
         self.board.__casillas__[23] = ["negro"]
         self.board.bornear_ficha(23, "negro")
         self.assertIn("negro", self.board.__fichas_retiradas__["negro"])
         self.assertEqual(self.board.__casillas__[23], [])

      def test_bornear_ficha_invalida(self):
         """No se puede retirar ficha si casilla vacía o color distinto."""
         with self.assertRaises(ValueError):
            self.board.bornear_ficha(0, "negro")  # en 0 hay blancas al inicio

      # --- Reinicio ---
      def test_reiniciar_tablero(self):
         """Reiniciar deja tablero en estado inicial."""
         self.board.__casillas__[0] = []
         self.board.__barra__["blanco"].append("blanco")
         self.board.reiniciar()
         self.assertEqual(self.board.__casillas__[0], ["blanco", "blanco"])
         self.assertEqual(self.board.__barra__, {"blanco": [], "negro": []})

   if __name__ == "__main__":
      unittest.main()
   ```
Salida: El código fue incorporado en el archivo `tests/test_board.py`. Se modificó el nombre de algunas variables y se incorporaron tests para casos como mover fichas fuera de rango o a casillas bloqueadas, enviar o retirar fichas desde posiciones inválidas y mover desde la barra a casillas no permitidas. Estos tests se agregaron ya que en el reporte de cobertura había lineas que no estaban cubiertas después de haber implementado la clase `Board`.