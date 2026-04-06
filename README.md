# Secure Password & Passphrase Generator

Herramienta CLI en Python para generar contraseñas y passphrases seguras usando aleatoriedad criptográficamente segura, políticas configurables y estimación teórica de entropía.

---

## Objetivo

El proyecto permite:

- generar contraseñas robustas con políticas configurables
- generar passphrases más memorables a partir de una wordlist
- estimar la entropía teórica de los valores generados
- separar la lógica de negocio de la interfaz CLI
- demostrar estructura real de proyecto Python en GitHub

---

## Características principales

### Generación de contraseñas

- longitud configurable
- inclusión o exclusión de mayúsculas, minúsculas, dígitos y símbolos
- exclusión opcional de caracteres ambiguos: `l`, `I`, `1`, `O`, `0`
- garantía de al menos un carácter por cada grupo seleccionado
- mezcla segura del resultado final

### Generación de passphrases

- selección aleatoria de palabras desde una wordlist local
- número de palabras configurable
- separador configurable
- opciones de capitalización
- posibilidad de añadir número y símbolo al final

### Estimación de entropía

- cálculo teórico basado en longitud y tamaño del conjunto de búsqueda
- cálculo para passphrases basado en tamaño de wordlist y número de palabras
- clasificación orientativa para contraseñas: baja, media, alta, muy alta

### Calidad del proyecto

- arquitectura modular
- validación de configuración
- tests unitarios
- sin dependencias externas obligatorias

---

## Estructura del proyecto

```text
secure-password-generator/
├── .gitignore
├── LICENSE
├── README.md
├── generator.py
├── passphrase_utils.py
├── password_utils.py
├── requirements.txt
├── exports/
├── tests/
│   ├── test_passphrase_utils.py
│   └── test_password_utils.py
└── wordlists/
    └── eff_large_wordlist.txt
```

---

## Arquitectura

### `generator.py`

Punto de entrada CLI. Gestiona argumentos y ofrece dos modos:

- `password`
- `passphrase`

### `password_utils.py`

Contiene la lógica de:

- construcción de conjuntos de caracteres
- validación de configuración
- generación de contraseñas
- estimación de entropía
- clasificación de fortaleza

### `passphrase_utils.py`

Contiene la lógica de:

- carga de la wordlist
- generación de passphrases
- cálculo de entropía teórica para frases

### `tests/`

Incluye pruebas unitarias para validar comportamiento básico.

---

## Decisiones de diseño

### Uso de `secrets`

La generación se basa en `secrets` en lugar de `random`.

Motivo:

- `random` no está diseñado para material sensible
- `secrets` utiliza fuentes de entropía adecuadas para seguridad

### Garantía de cumplimiento de política

En el modo contraseña no se elige todo desde un pool único sin control. Primero se fuerza al menos un carácter por grupo activo y después se completa el resto. Esto evita contraseñas que aparentan cumplir una política pero no la satisfacen realmente.

### Separación de responsabilidades

La lógica de negocio no está mezclada con la CLI. Esto facilita:

- mantenimiento
- testeo
- reutilización futura como librería o API

### Entropía como estimación teórica

La entropía mostrada es una estimación matemática, no una medida exacta de resistencia real frente a ataques dirigidos o contraseñas generadas por humanos.

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/secure-password-generator.git
cd secure-password-generator
```

Crear entorno virtual en Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

Este proyecto no requiere paquetes externos para funcionar en su versión actual.

---

## Uso

### Generar una contraseña

```bash
python generator.py password
```

### Generar varias contraseñas de 20 caracteres excluyendo ambiguos

```bash
python generator.py password --length 20 --count 3 --exclude-ambiguous
```

### Generar una contraseña sin símbolos

```bash
python generator.py password --no-symbols
```

### Generar una passphrase

```bash
python generator.py passphrase
```

### Generar una passphrase de 6 palabras capitalizadas

```bash
python generator.py passphrase --words 6 --capitalize
```

### Generar una passphrase con separador personalizado, número y símbolo

```bash
python generator.py passphrase --words 5 --separator "_" --add-number --add-symbol
```

---

## Ejemplo de salida

```text
[1] xT7@kL9!qW2#nP4$
    Fortaleza: Muy fuerte
    Entropía estimada: 104.23 bits (Muy alta)
```

```text
[1] faro-nube-mar-lince-cobre-sol
    Entropía estimada: 67.50 bits
```

---

## Testing

Ejecutar todos los tests:

```bash
python -m unittest discover tests
```

Los tests validan, entre otras cosas:

- longitud de la contraseña
- presencia de tipos de caracteres seleccionados
- validación de configuraciones inválidas
- generación de passphrases
- cálculo positivo de entropía

---

## Limitaciones actuales

- la entropía es una estimación teórica

---

## Posibles mejoras futuras

- integración con `zxcvbn`
- exportación cifrada opcional
- empaquetado con `pyproject.toml`
- distribución como comando instalable
- interfaz gráfica con Tkinter o CustomTkinter
- pipeline CI con GitHub Actions

---

## Licencia

MIT License

---
