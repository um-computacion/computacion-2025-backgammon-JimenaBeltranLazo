# 🎲 Backgammon: Computación 2025

## 👤 Información del Alumno

### 📋 Datos Personales
* **Nombre y Apellido**: Jimena Sofía Beltran Lazo
* **Ciclo Lectivo**: 2025
* **Carrera**: Ingeniería en Informática

## Resumen del Proyecto

Este proyecto consiste en la implementación del juego de **Backgammon** utilizando el lenguaje de programación Python. El desarrollo se ha centrado en separar la lógica de negocio (`core/`) de las capas de presentación, siguiendo los principios SOLID.

La aplicación resultante permite a los usuarios jugar partidas en dos modalidades:
1. **Versión de Consola (CLI):** Interacción basada en texto.
2. **Versión Gráfica (Pygame):** Interfaz visual con interacción por ratón y teclado.

-----

## 🛠️ Requisitos e Instalación

### Requisitos del Sistema
Se requiere tener instalado **Python 3.x** y el gestor de paquetes **PIP**.

### Dependencias del Proyecto

Todas las dependencias necesarias para la ejecución y el testing están listadas en el archivo `requirements.txt`.

Para instalar todas las librerías requeridas, ejecuta el siguiente comando en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

-----

## Cómo Ejecutar el Juego

El punto de entrada principal a la aplicación es el archivo `main.py`, que te permite seleccionar la interfaz deseada al inicio.

### Iniciar la Aplicación

Ejecuta el siguiente comando para iniciar el menú principal:

```bash
python main.py
```

Al ejecutarlo, se te presentará un menú interactivo:

1.  **Versión de Consola:** Inicia el juego en la terminal (CLI).
2.  **Versión con Pygame:** Inicia el juego con la interfaz gráfica.

-----

## 🧪 Modo Testing (Pruebas y Cobertura)

El proyecto incluye una suite de pruebas unitarias en la carpeta `tests/` para validar al menos el 90% de la lógica central del juego.

### 1\. Ejecutar las Pruebas Unitarias

Para ejecutar todos los tests que utilizan el módulo estándar de Python (`unittest`):

```bash
python -m unittest
```

### 2\. Ejecutar Pruebas con Reporte de Cobertura

Para ejecutar las pruebas y, a continuación, generar el reporte de cobertura de código (requiere la librería `coverage`):

```bash
coverage run -m unittest ; coverage report -m
```

**Resultado:** Este comando te mostrará un resumen detallado que indica el porcentaje de cobertura de cada módulo, siendo obligatorio alcanzar al menos el **90%** en los módulos de la lógica central (`core/`).

-----

## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular para garantizar la separación de responsabilidades:

```
/backgammon/
├── core/                         # Lógica central del juego
├── cli/                          # Interfaz de Línea de Comandos (CLI)
├── pygame_ui/                    # Interfaz Gráfica con Pygame
├── tests/                        # Tests unitarios
├── docs/                         # Archivos de justificación y documentación
│   ├── CHANGELOG.md              # Registro de cambios
│   └── JUSTIFICACION.md          # Justificación del diseño
├── prompts/                      # Archivos de prompts de IA utilizados
│   ├── prompts-desarrollo.md
│   ├── prompts-testing.md
│   └── prompts-documentacion.md
├── main.py                       # Punto de entrada principal
├── requirements.txt              # Listado de dependencias de Python
└── ...                           # Otros archivos de configuración (.gitignore, .pylintrc, etc.)
```