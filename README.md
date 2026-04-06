# Secure Password Generator

Herramienta CLI de Python para generar contraseñas seguras utilizando aleatoriedad criptográficamente segura, políticas de caracteres configurables, exclusión de caracteres ambiguos y estimación de fuerza básica.

## Características

- Longitud configurable
- Inclusión o exclusión de mayúsculas, minúsculas, números y símbolos
- Exclusión opcional de caracteres ambiguos
- Garantía de al menos un carácter por grupo seleccionado
- Estimación de fortaleza y entropía aproximada
- Tests básicos incluidos
- Sin dependencias externas

## Requisitos

- Python 3.10 o superior

## Uso

Ejemplo básico:

```bash
python generator.py
```

Generar 3 contraseñas de 20 caracteres excluyendo caracteres ambiguos:

```bash
python generator.py --length 20 --count 3 --exclude-ambiguous
```

Generar una contraseña sin símbolos:

```bash
python generator.py --no-symbols
```

## Ejemplo de salida

```text
Contraseña 1: wR7@kL9!qW2#nP4$
Fortaleza: Muy fuerte
Entropía estimada: 104.87 bits
----------------------------------------
```

## Seguridad

Este proyecto usa el módulo `secrets`, adecuado para generar valores aleatorios con fines de seguridad.

## Ejecutar tests

```bash
python -m unittest discover tests
```

## Licencia

MIT
