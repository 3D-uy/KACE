# Guía de Pruebas de KACE

Este documento explica cómo ejecutar la suite de pruebas de KACE, qué hace cada modo, cómo funciona el sistema de instantáneas (snapshots) y cómo está estructurado el pipeline de CI.

---

## Inicio Rápido

```bash
# Ejecutar la suite de pruebas completa (unitarias + regresión)
python3 tests/run_tests.py

# Verbose — ver cada nombre de prueba y PASS/FAIL
python3 tests/run_tests.py --verbose

# Validar el esquema y la precedencia de data/boards.yaml
python3 tests/run_tests.py --yaml-check

# Actualizar las instantáneas doradas después de un cambio de salida intencional
python3 tests/run_tests.py --update-snapshots

# Ejecutar el barrido completo de más de 192 configuraciones de Klipper (requiere red + git)
python3 tests/run_tests.py --full-klipper-sweep
```

---

## Categorías de Pruebas

### Pruebas Unitarias — `tests/unit/`

Pruebas rápidas y aisladas sin dependencias externas. Cada prueba simula (mock) todo lo que requeriría acceso a la red, avisos interactivos o hardware.

| Archivo | Qué prueba |
|------|--------------|
| `test_derivation.py` | Lógica de derivación MCU → Kconfig, coincidencia de patrones, respaldo (fallback) |
| `test_yaml_db.py` | Carga de YAML, validación del orden de patrones, recuperación de YAML dañado |
| `test_scraper.py` | Inyección de pines BLTouch a partir de la coincidencia de nombres de archivo |
| `test_deployer.py` | Instalación diferida de paramiko, manejo de fallos de red/fuera de línea |

### Pruebas de Regresión — `tests/regression/`

Pruebas basadas en instantáneas que renderizan un `printer.cfg` completo a partir de una configuración de Klipper simulada y lo comparan byte por byte con un archivo de referencia dorado (golden fixture).

| Archivo | Placas cubiertas |
|------|---------------|
| `test_config_generation.py` | SKR v1.4 (LPC1769) |
| `test_snapshot_expansion.py` | Creality v4.2.2, Creality v4.2.7, Octopus v1.1, SKR Pico (RP2040), SKR v1.3 (LPC1768), SKR Mini E3 sensorless |

---

## Sistema de Instantáneas (Snapshots)

Las instantáneas son archivos de salida dorados almacenados en `tests/fixtures/*.txt`. Cada archivo contiene la salida de `printer.cfg` esperada para una placa + configuración específica.

### Cómo funciona la comparación

`KaceTestCase.assertSnapshot()` en `tests/kace_test_case.py`:

1. Genera un `printer.cfg` a partir de datos simulados en un archivo temporal.
2. Lee el contenido del archivo temporal.
3. Elimina los espacios en blanco finales de cada línea.
4. Compara el contenido limpio con el archivo dorado almacenado.
5. Falla con un diff claro si algún carácter difiere.

La eliminación de espacios en blanco hace que las comparaciones sean estables entre plataformas (Windows CRLF vs Linux LF) sin ocultar diferencias reales.

### Actualizar instantáneas intencionalmente

Ejecuta con `--update-snapshots` cuando realices un cambio **deliberado** en el formato de salida:

```bash
python3 tests/run_tests.py --update-snapshots
```

Esto sobrescribe los archivos dorados. Siempre:
1. Revisa el git diff de cada archivo de fixture cambiado.
2. Verifica que los cambios sean los que pretendías.
3. Confirma (commit) las instantáneas actualizadas junto con el cambio de código.

> **Nunca** actualices las instantáneas silenciosamente como parte de un cambio no relacionado. Un cambio de instantánea es un cambio de contrato.

### Agregar una nueva instantánea

1. Agrega un nuevo método de prueba a `tests/regression/test_snapshot_expansion.py` siguiendo el patrón existente.
2. Ejecuta `python3 tests/run_tests.py --update-snapshots` para generar el fixture.
3. Ejecuta `python3 tests/run_tests.py --verbose` para confirmar que la nueva prueba pasa.
4. Realiza el commit tanto de la prueba como del archivo de fixture.

---

## Verificación de Integridad de YAML

```bash
python3 tests/run_tests.py --yaml-check
```

Esta comprobación independiente valida `data/boards.yaml` sin ejecutar ninguna prueba:

- Las claves de nivel superior (`boards`, `mcu_firmware`) deben estar presentes.
- Cada entrada de `boards[]` debe tener `mcu`, `search_terms` y `bltouch`.
- Cada entrada de `mcu_firmware[]` debe tener `pattern` y `arch`.
- Ningún patrón genérico puede sombrear un patrón más específico que aparezca más tarde (validación de precedencia).

Código de salida 0 = válido, código de salida 1 = errores encontrados con detalles impresos.

---

## Barrido Completo de Klipper

```bash
python3 tests/run_tests.py --full-klipper-sweep
```

El barrido:
1. Clona el repositorio de Klipper con `--depth 1 --sparse` (solo config/).
2. Itera cada `generic-*.cfg` y `printer-*.cfg`.
3. Ejecuta `parse_config()` + `extract_profile_defaults()` en cada uno.
4. Clasifica el resultado:

| Código | Significado |
|------|---------|
| `PASS` | El análisis completo + la extracción tuvieron éxito |
| `SAFE_ABORT` | Se encontraron pines de marcador de posición TODO — limitación elegante conocida |
| `UNSUPPORTED` | Secciones experimentales/no compatibles presentes |
| `FAILURE` | Excepción de Python no controlada — requiere investigación |

5. Imprime una tabla de estadísticas finales.
6. Sale con el código 1 si se registraron resultados de `FAILURE`.

El barrido requiere `git` en el `PATH` y acceso a la red. Se ejecuta automáticamente en cada push a `main` a través de GitHub Actions, pero se omite en los PRs para mantener rápida la iteración de los contribuidores.

---

## Resumen del Pipeline de CI

El flujo de trabajo de GitHub Actions en `.github/workflows/ci.yml` se ejecuta en cada push a `main` y en cada solicitud de extracción (pull request).

```
push / PR
    │
    ├── lint              — python -m py_compile (comprobación de sintaxis de todos los archivos .py)
    │
    ├── unit-tests        — ejecuta la suite de pruebas completa (21 pruebas)
    │
    ├── yaml-integrity    — comprobación de esquema + precedencia de boards.yaml
    │
    ├── regression-tests  — comparación de instantáneas (bloquea la fusión en caso de diferencias)
    │       └── needs: [unit-tests, yaml-integrity]
    │
    └── full-klipper-sweep  (SOLO push a main)
            └── needs: regression-tests
```

Todos los trabajos utilizan la cancelación de `concurrency`: si envías varios commits rápidamente al mismo PR, las ejecuciones de CI más antiguas se cancelan automáticamente.

### Reglas de bloqueo

Las fusiones a `main` se bloquean si falla cualquiera de los siguientes trabajos:
- `lint`
- `unit-tests`
- `yaml-integrity`
- `regression-tests`

El `full-klipper-sweep` es informativo en main (no bloquea los PRs).

---

## Diseño de Cero Dependencias

El ejecutor de pruebas utiliza solo módulos de la biblioteca estándar de Python:

```
unittest, sys, os, time, argparse, subprocess, tempfile, re
```

Esto significa que las pruebas pueden ejecutarse en una Raspberry Pi Zero 2W sin instalaciones de pip más allá del propio `requirements.txt` del proyecto. La suite completa se completa en menos de 0,5 segundos en hardware típico.
