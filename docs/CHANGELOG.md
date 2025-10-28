# CHANGELOG: Registro de Cambios

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere al [Versionamiento Semántico](https://semver.org/spec/v2.0.0.html).

## [0.5.0]- 2025-10-29
*(Periodo del 16 al 29 de Octubre. [...] commits en este período)*

### Added
- **Documentación de Prompts (Desarrollo):** Inclusión de los prompts utilizados en el desarrollo y la implementación de SOLID en la clase `CLI`.
- **Documentación de Prompts (Testing):** Inclusión de los prompts relacionados con el arreglo de los tests para alcanzar la cobertura de código requerida.
### Changed
- **Refactorización de Interfaz (SOLID):** Aplicación completa de los Principios SOLID a la `CLI`, lo que implicó dividir la clase en seis clases (`CLIBuilder`, `CLIInput`, `CLICommandParser`, `CLIPresenter`, `CLIGameExecutor` y `CLI`).
- **Implementación de Fachada en `BackgammonGame`:** Adición de múltiples métodos nuevos en `BackgammonGame` que simplifican el trabajo de CLI (como métodos para "tirar los dados" o "ver el tablero").
- **Implementación de Reglas de Captura:** Adición de la lógica que faltaba en el `Board` para manejar la captura de fichas enemigas solas en un destino y su envío a la barra.
- **Estabilización de Interfaz:** Modificación y refactorización de los archivos `cli.py` y `main.py` para que la Interfaz de Línea de Comandos sea estable y funcione correctamente al iniciar y durante el juego.
### Fixed
- **Aseguramiento de Cobertura y Estabilidad:** Adición de casos de prueba unitarios en `CLI`, `Board` y `BackgammonGame` para garantizar la cobertura de líneas. Esto incluye:
    * Verificación de la lógica de la barra (reingreso, bloqueo, captura).
    * Validación de flujo de turno (fin de turno, continuación, detección de victoria).
    * Manejo de errores de formato y comandos ilegales en la `CLICommandParser`.
    * Pruebas de la nueva Inyección de Dependencias y los métodos de la `CLIPresenter`.

---
## [0.4.0] - 2025-10-15
*(Periodo del 02 al 15 de Octubre. 10 commits en este período)*

### Added
- **Implementación de Interfaz (`CLI`):** Desarrollo de la clase `CLI` (Command Line Interface) con sus tests unitarios iniciales, permitiendo la primera ejecución de prueba del juego.
- **Implementación de `Main`:** Inclusión del archivo `main.py` para la ejecución directa del proyecto. *Nota: Este archivo fue añadido como un checkpoint y presenta errores al momento de ejecutar la CLI.*
- **Documentación de Prompts:** Inclusión de todos los prompts utilizados para desarrollar, aplicar y testear la refactorización de las clases Core con los principios SOLID.
### Changed
- **Implementación de Principios SOLID:** Aplicación de los Principios SOLID a las clases principales (`Dice`, `Board`, `BackgammonGame`) para mejorar la modularidad, extensibilidad y calidad del código.
- **Reorganización de Lógica Core:** Reestructuración de las clases principales del Core para reflejar la aplicación de SOLID, incluyendo la creación de nuevas clases de gestión de lógica (`DiceGameLogic`, `SquareManager`, `BarManager`, `TurnManager` y `MoveManager`).
- **Normalización de Código y Tests:** Ajuste de los tests y clases para respetar el uso de doble guion bajo en los atributos privados.
### Fixed
- **Corrección de Configuración del Coverage:** Arreglo en el archivo `.coveragerc` para excluir los archivos `__init__.py` del reporte de cobertura, asegurando una medición del porcentaje más precisa.

---
## [0.3.0] - 2025-10-01
*(Periodo del 18 de Septiembre al 01 de Octubre. 7 commits en este período)*

### Added
- **Implementación de la Clase Principal (`BackgammonGame`):** Desarrollo e inclusión de la clase `BackgammonGame`, la lógica central para gestionar el flujo de la partida.
- **Implementación de Tests (`BackgammonGame`):** Desarrollo de las pruebas unitarias para la clase `BackgammonGame`, con inclusión de ajustes de variables y expansión de tests para alcanzar la cobertura total de líneas.
- **Documentación de Prompts:** Inclusión de todos los prompts utilizados en el desarrollo y testeo de la clase `BackgammonGame`.
### Changed
- **Refinamiento de Lógica de `Board`:** Modificación en la clase `Board` (introducida en `[0.2.0]`) con la adición de nuevas validaciones de movimiento. Esto asegura que se cumplan las reglas de la barra y el destino de la ficha antes de moverla.
- **Revisión de Tests Críticos:** Reescritura completa del archivo de tests de `BackgammonGame` (que se había creado al inicio del sprint) para corregir errores de implementación.

---
## [0.2.0] - 2025-09-17
*(Periodo del 04 al 17 de Septiembre. 12 commits en este período)*

### Added
- **Implementación de la CLase `Checker`:** Desarrollo de la clase `Checker`.
- **Implementación de la Clase `Player` + Tests:** Inclusión de la clase funcional `Player` con sus tests unitarios.
- **Implementación de la Clase `Board` + Tests:** Inclusión de la clase `Board` con ajustes en sus tests para alcanzar la cobertura total.
- **Configuración de Integración Continua:** Creación de los archivos `.pylintrc` y `ci.yml` para habilitar la Integración Continua (GitHub Actions), permitiendo la verificación automática de calidad de código.
- **Documentación de Prompts:** Inclusión de todos los prompts utilizados en el desarrollo y testeo de las clases `Checker`, `Player` y `Board`.
### Changed
- **Reorganización Estructural:** Reorganización de la arquitectura de archivos; los documentos `CHANGELOG.md` y `JUSTIFICACION.md` fueron movidos a la carpeta `docs/`. Inclusión de archivos `__init__.py` en las carpetas principales para su correcta identificación como paquetes modulares de Python.
- **Normalización de Código:** Ajuste en los tests de la clase `Checker` para respetar la convención obligatoria de usar doble guion bajo (`__`) en los atributos privados.
- **Configuración de Dependencias:** Actualización del archivo `requirements.txt` con nuevas librerías para herramientas de calidad (`pylint`).
### Fixed
- **Corrección de Integración Continua:** Solución de un error generado en la configuración inicial del workflow de GitHub Actions para asegurar que los reportes se guarden de forma correcta y organizada en la nueva carpeta `reports/`.

---
## [0.1.0] - 2025-09-03
*(Periodo del 20 de Agosto al 03 de Septiembre. 7 commits en este período)*

### Added
- **Organización de la Estructura Base del Proyecto:** Creación de todas las carpetas del proyecto (`core`, `tests`, `pygame_ui`, `cli`, etc.) y de los archivos de documentación inicial (`README.md`, `CHANGELOG.md` y `JUSTIFICACION.md`).
- **Configuración Inicial:** Preparación del entorno virtual (`venv`), definición de los archivos `.gitignore`, `coveragerc` y `requirements.txt` para la gestión de dependencias y calidad.
- **Implementación de Tests `Dice`:** Desarrollo de los tests unitarios para la clase `Dice`.
- **Implementación de la Clase `Dice`:** Inclusión de la clase funcional `Dice` con algunos ajustes en sus tests unitarios.
- **Documentación de Presentación:** Actualización del `README.md` con el título del proyecto, datos del alumno, y los comandos de ejecución de tests y verificación de cobertura.
- **Documentación de Prompts:** Inclusión de los prompts utilizados para desarrollar y testear la clase `Dice`.
- **Preparación de Tests `Checker`:** Implementación de los tests unitarios iniciales para la futura clase `Checker`.

---