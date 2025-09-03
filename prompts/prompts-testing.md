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
Salida: El código fue incorporado al archivo `tests/test_dice.py`. Se modificó el nombre de las funciones y algunas variables, y siguiendo la lógica del mismo código, se incorporó que verifique que cuando se obtiene doble la cantidad de movimientos sea 4.