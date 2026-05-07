# Changelog

All notable changes to KACE are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
KACE uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `--full-klipper-sweep` flag: clones Klipper shallowly and validates all 192+ official configs
- `--yaml-check` flag: validates `data/boards.yaml` schema, required keys, and pattern precedence
- `tests/sweep/result_codes.py`: four-code classification system (`PASS`, `SAFE_ABORT`, `UNSUPPORTED`, `FAILURE`)
- `tests/sweep/klipper_sweep.py`: offline-safe sweep engine with sparse git checkout
- Six new regression snapshot fixtures: Creality v4.2.2, Creality v4.2.7, Octopus v1.1, SKR Pico (RP2040), SKR v1.3 (LPC176x), SKR Mini E3 sensorless
- `VERSION` file: single source of truth for the project version
- `docs/RELEASE.md`: release engineering guide (versioning, tagging, rollback)
- `docs/en/ARCHITECTURE.md`: YAML schema reference, derivation pipeline, fallback logic
- `docs/en/TESTING.md`: test suite usage, snapshot system, CI workflow
- `docs/en/CONTRIBUTING.md`: board addition guide, PR checklist
- `.github/workflows/ci.yml`: full GitHub Actions CI pipeline with concurrency cancellation

### Changed
- `tests/run_tests.py`: added `--yaml-check` and `--full-klipper-sweep` flags; improved help text
- `kace.py`: `--version` flag now reads from `VERSION` file; `__version__` kept in sync

---

## [0.1.0] — 2026-05-07

### Added
- MCU auto-detection via USB/serial (`firmware/detector.py`)
- GitHub configuration scraper with 3-day cache and HTML fallback (`core/scraper.py`)
- Intelligent configuration engine — parses Klipper configs, extracts profile defaults
- Jinja2-based `printer.cfg` generator with comment alignment and translation support
- Firmware derivation engine (`firmware/derivation.py`) with YAML-backed pattern database
- Interactive CLI wizard — 14-step guided flow (`core/wizard.py`)
- Multi-language support: English, Spanish, Portuguese (`core/translations.py`)
- System status dashboard — detects Klipper, Moonraker, Mainsail, Fluidd, Crowsnest, MCU
- Modular hardware database (`data/boards.yaml`) — boards, BLTouch overrides, firmware patterns
- Fallback system — every YAML load has a hardcoded fallback dict preventing regressions
- Automated test runner framework (`tests/run_tests.py`) — zero external dependencies
- Snapshot regression testing against golden `.txt` fixtures (`tests/fixtures/`)
- SSH deployment via on-demand `paramiko` install (`core/deployer.py`)
- USB/SD card deployment support
- BLTouch pin injection from modular YAML database
- `--auto` flag for CI/headless operation
- Sparse + shallow git clone installer (`install.sh`)
- ANSI colour-coded terminal UI with emoji icon menus
- Validated against 192 official Klipper board configurations

[Unreleased]: https://github.com/3D-uy/kace/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/3D-uy/kace/releases/tag/v0.1.0
