# KACE Architecture Reference

This document is the canonical reference for the KACE system architecture.
It covers the YAML schema, derivation pipeline, fallback logic, and precedence rules.

---

## 1. YAML Schema — `data/boards.yaml`

The hardware database is the single source of truth for all board-specific data.
Adding a new board or BLTouch override requires **only a YAML edit** — no Python changes.

### Top-level keys

```yaml
boards:       # List — board definitions (MCU search terms, BLTouch pins, features)
mcu_firmware: # List — firmware derivation patterns (ordered most-specific first)
```

### `boards[]` entry schema

```yaml
- mcu: <string>            # MCU chip prefix matching firmware/detector.py output
                           # e.g. "stm32f103", "lpc1769", "rp2040"

  search_terms:            # List of substrings matched against Klipper config filenames
    - skr-v1.4             # e.g. matches "generic-bigtreetech-skr-v1.4.cfg"
    - skr-v1.3

  bltouch:                 # Map: board-filename-fragment → BLTouch pin overrides
    skr-v1.4:              # Key must be a substring of the Klipper config filename
      sensor_pin: "^P0.10" # BLTouch Z-min / sensor pin (with ^ pull-up if needed)
      control_pin: "P2.0"  # BLTouch servo / control pin
    skr-v1.3:
      sensor_pin: "^P1.27"
      control_pin: "P2.0"

  features:                # (Future use) Hardware capabilities for adaptive menus
    uart: true
    sensorless: true
    input_shaper: false
```

### `mcu_firmware[]` entry schema

```yaml
- pattern: "stm32f103"    # Substring matched against detected MCU string (lowercase)
                          # ORDER MATTERS — most specific patterns must appear first
  arch: stm32             # CONFIG_MCU value (Klipper architecture string)
  mach: STM32             # CONFIG_MACH_{mach} suffix (omit for AVR/RP2040/linux)
  flash_start: "0x7000"   # CONFIG_FLASH_START hex string
                          #   absent  → no bootloader config needed (RP2040, AVR)
                          #   null    → ambiguous, wizard will prompt the user
                          #   "0x0"   → explicitly no offset, skip CONFIG_FLASH_START
                          #   "0xN"   → set CONFIG_FLASH_START = "0xN"
  clock_freq: 120000000   # (optional) CONFIG_CLOCK_FREQ in Hz
  set_mcu_flag: true      # (optional) also sets CONFIG_MCU_{detected_mcu.upper()} = y
  extra_flag: "CONFIG_MCU_ATMEGA2560"  # (optional) additional CONFIG_* key → y
  early_return: true      # (optional) return immediately after arch (Linux/host MCU)
```

---

## 2. Derivation Pipeline

The firmware derivation pipeline converts a detected MCU string into a complete
set of Kconfig parameters suitable for compiling Klipper firmware.

```
Detected MCU string  (e.g. "stm32f446xx")
         │
         ▼
  firmware/derivation.py — derive_config(mcu, hint)
         │
         ├─ 1. Load database (_FW_DB) from data/boards.yaml
         │      └─ fallback to _FW_DB_FALLBACK if YAML is missing/invalid
         │
         ├─ 2. Pattern match (first-match-wins, most-specific first)
         │      e.g. "stm32f446xx" matches pattern "stm32f4"
         │
         ├─ 3. Set CONFIG_MCU = "{arch}"
         │      e.g. CONFIG_MCU = "stm32"
         │
         ├─ 4. Set CONFIG_MACH_{mach} = y
         │      e.g. CONFIG_MACH_STM32 = y
         │
         ├─ 5. Set CONFIG_MCU_{mcu.upper()} = y  (if set_mcu_flag)
         │      e.g. CONFIG_MCU_STM32F446XX = y
         │
         ├─ 6. Resolve bootloader offset (flash_start)
         │      None present  → skip (RP2040, AVR)
         │      null in YAML  → prompt user via prompt_bootloader_offset()
         │      "0x0"         → no offset, skip CONFIG_FLASH_START
         │      "0xN"         → CONFIG_FLASH_START = "0xN"
         │
         ├─ 7. Set clock frequency (if clock_freq present)
         │
         ├─ 8. Set extra_flag (if present)
         │
         └─ 9. Derive communication interface
                hint provided  → use directly ("usb", "uart", "can", "spi")
                no hint        → prompt user via prompt_communication_interface()
                Result: CONFIG_USB / CONFIG_SERIAL / CONFIG_CANBUS / CONFIG_SPI
```

---

## 3. Fallback Logic

Every data-loading operation in KACE has a hardcoded fallback dict. This guarantees
zero regression risk on existing installs even if `data/boards.yaml` is missing,
corrupted, or from an older version.

| Module | Load function | Fallback constant |
|--------|--------------|-------------------|
| `firmware/derivation.py` | `_load_firmware_db()` | `_FW_DB_FALLBACK` |
| `core/scraper.py` | `_load_bltouch_db()` | `_BLTOUCH_FALLBACK` |
| `core/wizard.py` | `_load_mcu_search_terms()` | `_MCU_SEARCH_FALLBACK` |

Fallback triggers:
- YAML file does not exist
- YAML parse error (malformed syntax)
- Pattern precedence violation detected (shadowing)
- Any other `Exception` during load

When a fallback is used, KACE prints a yellow `[!] WARNING` to stdout with the
error detail. The application continues normally using the built-in defaults.

---

## 4. Precedence Rules

### YAML pattern order

In `mcu_firmware[]`, patterns are matched using **first-match-wins** substring
search. More specific patterns **must** appear before generic ones.

**Correct:**
```yaml
- pattern: "stm32f103"   # ← index 0: specific
- pattern: "stm32f1"     # ← index 1: less specific
- pattern: "stm32"       # ← index 2: generic fallback
```

**Wrong (will be caught and rejected):**
```yaml
- pattern: "stm32"       # ← too generic — shadows stm32f103 below!
- pattern: "stm32f103"   # ← will never be reached
```

The `_load_firmware_db()` validator checks every pair of entries and raises a
warning + falls back to built-in defaults if shadowing is detected.

### BLTouch board key matching

In `boards[].bltouch`, keys are matched as substrings of the Klipper config
filename. The **first matching key wins**. Board keys should be ordered from most
specific to most generic within the YAML entry (e.g. `skr-mini-e3-v2.0` before
`skr-mini-e3`).

---

## 5. Config Generation Pipeline

```
raw Klipper .cfg text
         │
         ▼
  core/scraper.py — parse_config(raw, filename)
         │   Extracts sections + key-value pairs
         │   Injects BLTouch pins from _BLTOUCH_DB
         │   Filters TODO pins in board_pins aliases
         │
         ▼
  core/scraper.py — extract_profile_defaults(parsed)
         │   Derives kinematics, sizes, thermistors, gear ratios
         │   Handles both rotation_distance and legacy step_distance
         │
         ▼
  core/wizard.py — run_wizard()
         │   Collects user choices (driver type, probe, language, etc.)
         │
         ▼
  core/generator.py — generate_config(parsed, user_data, output_path)
         │   Jinja2 renders templates/printer.cfg.j2
         │   Aligns inline comments to column 48
         │   Translates comments via core/translations.py
         │   Validates: no active TODO pins in output
         │   Writes ~/kace/printer.cfg
         │
         ▼
  printer.cfg  ✓
```

---

## 6. Module Map

| Path | Responsibility |
|------|---------------|
| `kace.py` | Entry point, argument parsing, phase orchestration |
| `core/scraper.py` | GitHub config fetch, parse, BLTouch injection, profile defaults |
| `core/generator.py` | Jinja2 rendering, comment alignment, TODO validation |
| `core/wizard.py` | 14-step interactive CLI wizard, MCU search term loading |
| `core/dashboard.py` | System status detection (Klipper, Moonraker, etc.) |
| `core/deployer.py` | Local / USB / SSH / avrdude deployment |
| `core/translations.py` | `t()` i18n layer, comment translation |
| `core/banner.py` | ANSI banner display |
| `core/style.py` | questionary colour theme |
| `firmware/derivation.py` | MCU → Kconfig parameter derivation |
| `firmware/builder.py` | Firmware compilation orchestration |
| `firmware/detector.py` | USB serial MCU detection |
| `firmware/prompts.py` | Interactive prompts for firmware config |
| `firmware/validator.py` | Pre-flight config validation |
| `data/boards.yaml` | Modular hardware database |
| `templates/printer.cfg.j2` | Jinja2 printer config template |
| `tests/run_tests.py` | Test runner entry point |
| `tests/sweep/` | Full Klipper sweep engine and result codes |
| `tests/regression/` | Snapshot regression tests |
| `tests/unit/` | Unit tests (derivation, YAML DB, scraper, deployer) |
| `tests/fixtures/` | Golden snapshot `.txt` files |
