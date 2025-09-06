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
Salida: El código fue incorporado en el archivo `tests/test_checker.py`. Se modificó nuevamente el nombre de algunas funciones y variables, y en test_desactivar_ficha se incorporó que la posición quede en None si la ficha ya no está en el tablero.