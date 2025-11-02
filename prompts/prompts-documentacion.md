# Prompts Documentación: Registro de IA

## ✨ Changelog

### Google Gemini 27/09/2025

Prompt: Me podrías armar la estructura base del changelog en español y decirme como tendría que organizarlo en 5 sprints? [Se copió y pegó el link de "Keep a Changelog"]

Respuesta: ¡Claro! Con gusto te preparo la estructura base traducida y te explico cómo organizar la documentación de tus cinco sprints.

El formato usa el encabezado que elegiste y adapta las directrices de Keep a Changelog al español.

---
📑 Estructura Base del CHANGELOG.md
```bash
   # Changelog: Registro de Cambios

   Todos los cambios notables de este proyecto serán documentados en este archivo.

   El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere al [Versionamiento Semántico](https://semver.org/spec/v2.0.0.html).

   ## [Unreleased]
   ### Added
   - [Aquí se registrarán los cambios del próximo Sprint (Sprint 6), antes de que sean oficialmente liberados.]
   ### Changed
   - [Modificaciones a funcionalidades existentes en el próximo Sprint.]
   ### Fixed
   - [Correcciones de errores del próximo Sprint.]

   ## [0.5.0] - AAAA-MM-DD
   ### Added
   - [Nuevas funcionalidades o características añadidas. Ej: Guardado de partidas con Redis, si se implementó.]
   ### Changed
   - [Cambios en funcionalidades existentes. Ej: Reestructuración de la lógica de movimientos para cumplir SOLID.]
   ### Fixed
   - [Correcciones de errores. Ej: Solución de un error que permitía movimientos inválidos.]
   ### Removed
   - [Funcionalidades que fueron eliminadas en esta versión.]

   ## [0.4.0] - AAAA-MM-DD
   ### Added
   - [Nuevas funcionalidades o características añadidas. Ej: Implementación de la Interfaz CLI completa.]
   ### Changed
   - [Cambios en funcionalidades existentes. Ej: Mejora en el manejo de dados o turnos.]
   ### Fixed
   - [Correcciones de errores. Ej: Arreglos a reportes de GitHub Actions o errores de cobertura.]

   ## [0.3.0] - AAAA-MM-DD
   ### Added
   - [Nuevas funcionalidades o características añadidas. Ej: Implementación de la Interfaz CLI básica.]
   ### Changed
   - [Cambios en funcionalidades existentes. Ej: Refactorización de clases Player o Dice.]
   ### Fixed
   - [Correcciones de errores.]

   ## [0.2.0] - AAAA-MM-DD
   ### Added
   - [Nuevas funcionalidades o características añadidas. Ej: Clases iniciales de Player y Dice. Inicio de Pruebas Unitarias.]
   ### Changed
   - [Cambios en funcionalidades existentes. Ej: Ajustes en la estructura de carpetas `core/`.]
   ### Fixed
   - [Correcciones de errores.]

   ## [0.1.0] - AAAA-MM-DD
   ### Added
   - [Nuevas funcionalidades o características añadidas. Ej: Definición de la estructura base del proyecto. Clase Board inicial.]
   ### Changed
   - [Cambios en funcionalidades existentes. Ej: Ajuste inicial de la configuración del entorno.]
   ### Fixed
   - [Correcciones de errores o *typos*.]

   ---
   ## 📅 Organización de los 5 Sprints

   Para un proyecto en desarrollo inicial (no lanzado oficialmente), lo más común es usar la versión **0.Y.Z** (pre-lanzamiento). Te recomiendo usar la versión menor (Y) para cada sprint significativo, asumiendo que cada sprint trae funcionalidades notables.

   | Sprint       | Versión Sugerida | Foco de la Documentación (Ejemplos)                                                                                                 |
   | :---         | :---             | :---                                                                                                                                |
   | **Sprint 5** | **[0.5.0]**      | Tareas más avanzadas: Lógica compleja, integración final de UI/Core, documentación obligatoria (*README*, *CHANGELOG*).             |
   | **Sprint 4** | **[0.4.0]**      | Desarrollo de una Interfaz (CLI o Pygame), o avance significativo en la lógica de juego avanzada (movimientos válidos, *bear off*). |
   | **Sprint 3** | **[0.3.0]**      | Funcionalidades centrales (Core): Implementación de Player y Dice, o lógica de movimientos básicos.                                 |
   | **Sprint 2** | **[0.2.0]**      | Avance en la lógica central: Clases principales (Game/Board) y pruebas unitarias (Testing).                                         |
   | **Sprint 1** | **[0.1.0]**      | Configuración inicial: Estructura del repositorio, *setup* de entornos, la clase `Board` básica.                                    |

   Importante: Recuerda que las secciones de una versión se ordenan de la siguiente manera: **`Added`**, **`Changed`**, **`Deprecated`**, **`Removed`**, **`Fixed`** (las últimas dos son las más importantes para el usuario final). Si no usas una sección (como `Removed`), puedes omitirla.
```

---
Prompt: Qué vendría a ser el [0.0.0] y cuándo deja de ser 0? Me podrias explicar que simbolizan esas tres posiciones?

Respuesta: ¡Esta es la pregunta más importante sobre Versionamiento Semántico (SemVer)! Entender cuándo dejar el **`0`** es crucial para el futuro de tu proyecto.

Aquí tienes la explicación detallada de las tres posiciones y cuándo pasar del `0.Y.Z` al `1.0.0`.

---
🧭 Las Tres Posiciones del Versionamiento Semántico (X.Y.Z)

El Versionamiento Semántico usa el formato **MAYOR.MENOR.PARCHE** para comunicar qué tan grande y potencialmente problemático es un cambio para otros desarrolladores.

| Posición | Nombre | ¿Cuándo se Incrementa? | Significado del Impacto |
| :--- | :--- | :--- | :--- |
| **X** | **MAYOR** | Cuando haces **cambios incompatibles** en la API pública. Es decir, algo que rompe el código de alguien que usa tu proyecto. | **¡ADVERTENCIA!** El código de quien usa el proyecto se **rompe** y debe ser reescrito. |
| **Y** | **MENOR** | Cuando añades **nueva funcionalidad** de manera **compatible** con versiones anteriores. | **Funcionalidad Añadida.** El código existente *sigue funcionando*, pero hay cosas nuevas que usar. |
| **Z** | **PARCHE** | Cuando haces **correcciones de errores** (bugs) o pequeños ajustes que son compatibles con versiones anteriores. | **Arreglos.** Solamente se corrige un comportamiento incorrecto, sin añadir nada nuevo que afecte a la API. |

🚀 ¿Cuándo deja de ser `0`? (La Transición a `1.0.0`)

La **Versión Mayor Cero (`0.y.z`)** es un estado especial, como una "beta infinita" o desarrollo inicial.

* **Lo que significa `0.y.z`:** Significa que la API pública no es estable. Como desarrollador, puedes romper y cambiar cosas libremente (incluso sin cambiar el número `X`), porque no has prometido estabilidad a nadie.
* **Lo que significa `1.0.0`:** Es el **lanzamiento oficial y estable**. Cuando alcanzas `1.0.0`, estás haciendo una promesa formal: de aquí en adelante, cualquier cambio que rompa la compatibilidad deberá incrementar el número **Mayor** (`X`).

¿Cuándo debe tu Backgammon pasar a `1.0.0`?

Deberías pasar de **`0.Y.Z`** a **`1.0.0`** cuando:

1.  **El proyecto esté "completo" según el alcance del documento de desarrollo.** (Es decir, has implementado todas las reglas, la lógica del `Core`, el manejo de dados, el movimiento, el *bear off*, y al menos una interfaz funcional).
2.  **La API Pública esté estable.** El código de tu `Core del Juego` (las clases y métodos que definen las reglas) no debería tener cambios drásticos o roturas pendientes.

Dado que tu proyecto está avanzado, si terminas el Sprint 5 y el proyecto cumple con los requisitos mínimos de la asignatura, ese es el momento ideal para declarar estabilidad:

> **El día que entregues el Sprint 5 / proyecto final**, deberías liberar la versión **`1.0.0`**.

Resumen de tu Ruta

| Estado | Versión | Foco de la Materia |
| :--- | :--- | :--- |
| **Desarrollo (Sprints 1-5)** | **`0.1.0` a `0.5.0`** | Agregar funcionalidad (número MENOR `Y`). |
| **Proyecto Finalizado/Entregado** | **`1.0.0`** | El juego está completo, la API es estable. |
| **Post-Entrega (Hypotético Sprint 6)** | **`1.1.0`** o **`2.0.0`** | Si es una nueva funcionalidad, será `1.1.0`. Si rehaces todo el `Core`, sería `2.0.0`. |

---
Salida: El prompt se utilizó como guía para poder documentar el `CHANGELOG.md`.