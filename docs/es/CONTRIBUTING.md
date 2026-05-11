# Contribuyendo a KACE

Gracias por considerar una contribución a KACE.
Esta guía explica cómo agregar nuevas placas, crear instantáneas (snapshots) y enviar PRs seguros.

---

## Configuración de Desarrollo

```bash
git clone https://github.com/3D-uy/kace.git
cd kace
pip install -r requirements.txt
```

Ejecuta la suite de pruebas para verificar tu entorno:

```bash
python3 tests/run_tests.py --verbose
```

Las 21 pruebas deben pasar antes de que se acepte cualquier contribución.

---

## Agregar una Nueva Placa

Los datos de las placas de KACE residen enteramente en `data/boards.yaml`. Agregar una nueva placa
requiere **solo una edición de YAML** — no se necesitan cambios en Python.

### Paso 1 — Agrega la placa a `boards[]`

Busca (o crea) el grupo `mcu` correcto y agrega el término de búsqueda de tu placa:

```yaml
boards:
  - mcu: stm32f103
    search_terms:
      - creality-v4.2.2
      - creality-v4.2.7
      - skr-mini-e3
      - tu-nueva-placa      # ← agregar aquí
    bltouch:
      tu-nueva-placa:       # ← subcadena del nombre de archivo de configuración de Klipper
        sensor_pin: "^PA7"  # Pin Z-min con pull-up si es necesario
        control_pin: "PB0"  # Pin de servo/control
```

Las entradas de la lista `search_terms` deben ser subcadenas del nombre oficial del archivo de
configuración de Klipper (ej. `generic-tu-nueva-placa.cfg` → `tu-nueva-placa`).

Si tu placa utiliza un MCU diferente que aún no está listado, agrega una nueva entrada `boards[]`
con el valor de `mcu` correcto de `firmware/detector.py`.

### Paso 2 — Verifica que el patrón de firmware exista

Comprueba que `mcu_firmware[]` tenga un patrón para la familia MCU de tu placa.
Si tu placa usa `stm32f103`, `stm32f4`, `lpc1769` o `rp2040`, ya está cubierta. Si necesitas una nueva familia de MCU, agrega una nueva entrada:

```yaml
mcu_firmware:
  - pattern: "tu-nuevo-mcu"   # debe estar antes de cualquier patrón padre genérico
    arch: stm32
    mach: STM32
    flash_start: "0x8000"
    set_mcu_flag: true
```

> **El orden importa.** Los patrones más específicos deben aparecer antes que los genéricos.
> Ejecuta `python3 tests/run_tests.py --yaml-check` para validar la precedencia.

### Paso 3 — Valida el YAML

```bash
python3 tests/run_tests.py --yaml-check
```

Esto verifica el esquema, los campos obligatorios y el orden de los patrones. Corrige cualquier error antes de continuar.

### Paso 4 — Agrega una instantánea de regresión (regression snapshot)

Crea una cadena de configuración simulada en `tests/regression/test_snapshot_expansion.py`
siguiendo los ejemplos existentes:

```python
MOCK_TU_PLACA = """
[stepper_x]
step_pin: PA0
...
"""

def test_tu_placa_snapshot(self):
    """Instantánea de regresión para Tu Placa (STM32Fxxx)."""
    self._run_snapshot(
        "tu-placa-esperada",
        MOCK_TU_PLACA,
        "generic-tu-nueva-placa.cfg",
        "/dev/serial/by-id/usb-Klipper_stm32fxxx_mock-if00",
    )
```

Genera el fixture dorado (golden fixture):

```bash
python3 tests/run_tests.py --update-snapshots
```

Verifica que la instantánea se vea correcta y luego ejecuta la suite completa:

```bash
python3 tests/run_tests.py --verbose
```

### Paso 5 — Envía tu PR

Todas las 21+ pruebas deben pasar. El pipeline de CI se ejecutará automáticamente en tu PR.

---

## Lista de Verificación del PR

Antes de abrir un PR, verifica todo lo siguiente:

- [ ] `python3 tests/run_tests.py --verbose` → todas las pruebas pasan
- [ ] `python3 tests/run_tests.py --yaml-check` → YAML válido
- [ ] Archivos de instantáneas confirmados junto con los cambios de código (si el resultado cambió)
- [ ] Sección `[Unreleased]` de `CHANGELOG.md` actualizada
- [ ] No se agregaron cadenas de texto en inglés a la interfaz (usa `t()` de `core/translations.py`)
- [ ] No se agregaron llamadas a `sys.exit()` fuera del punto de entrada `kace.py`
- [ ] No se agregaron nuevas dependencias externas sin discusión previa

---

## Estilo de Código

- Las características de Python 3.11+ están bien.
- Sigue los patrones existentes en cada módulo — no nuevas capas de abstracción.
- Todos los datos de las placas van en `data/boards.yaml`, no en Python.
- Todas las cadenas orientadas al usuario pasan por `t()`, no están codificadas (hardcoded).
- Todos los módulos nuevos que cargan datos opcionales deben tener un diccionario de respaldo codificado.

---

## Congelación de Arquitectura

La arquitectura central es intencionalmente estable. Por favor, no propongas:

- Nuevas capas de abstracción en `core/` o `firmware/`
- Cambios de esquema en `boards.yaml` sin discusión previa
- Cambios en la plantilla Jinja2 que rompan silenciosamente las instantáneas existentes

Si se necesita una refactorización mayor, abre primero un problema (issue) describiendo la motivación.

---

## Obtener Ayuda

Abre un problema en [GitHub](https://github.com/3D-uy/kace/issues) con:
- Tu modelo de placa
- El nombre del archivo de configuración de Klipper (`generic-xxx.cfg`)
- El chip MCU de tu placa
- Qué genera KACE actualmente frente a lo que esperas
