# KACE Testing Guide

This document explains how to run the KACE test suite, what each mode does,
how the snapshot system works, and how the CI pipeline is structured.

---

## Quick Start

```bash
# Run the full test suite (unit + regression)
python3 tests/run_tests.py

# Verbose — see each test name and PASS/FAIL
python3 tests/run_tests.py --verbose

# Validate data/boards.yaml schema and precedence
python3 tests/run_tests.py --yaml-check

# Update golden snapshots after an intentional output change
python3 tests/run_tests.py --update-snapshots

# Run the full Klipper 192+ config sweep (requires network + git)
python3 tests/run_tests.py --full-klipper-sweep
```

---

## Test Categories

### Unit Tests — `tests/unit/`

Fast, isolated tests with no external dependencies. Each test mocks everything
that would require network access, interactive prompts, or hardware.

| File | What it tests |
|------|--------------|
| `test_derivation.py` | MCU → Kconfig derivation logic, pattern matching, fallback |
| `test_yaml_db.py` | YAML load, pattern order validation, broken-YAML recovery |
| `test_scraper.py` | BLTouch pin injection from filename matching |
| `test_deployer.py` | Lazy paramiko installation, offline/network-failure handling |

### Regression Tests — `tests/regression/`

Snapshot-based tests that render a complete `printer.cfg` from a mock Klipper
config and compare it byte-for-byte against a golden fixture file.

| File | Boards covered |
|------|---------------|
| `test_config_generation.py` | SKR v1.4 (LPC1769) |
| `test_snapshot_expansion.py` | Creality v4.2.2, Creality v4.2.7, Octopus v1.1, SKR Pico (RP2040), SKR v1.3 (LPC1768), SKR Mini E3 sensorless |

---

## Snapshot System

Snapshots are golden output files stored in `tests/fixtures/*.txt`. Each file
contains the expected `printer.cfg` output for a specific board + configuration.

### How comparison works

`KaceTestCase.assertSnapshot()` in `tests/kace_test_case.py`:

1. Generates a `printer.cfg` from mock data into a temp file.
2. Reads the temp file content.
3. Strips trailing whitespace from every line.
4. Compares stripped content against the stored golden file.
5. Fails with a clear diff if any character differs.

The whitespace-stripping makes comparisons stable across platforms (Windows CRLF
vs Linux LF) without hiding real differences.

### Updating snapshots intentionally

Run with `--update-snapshots` when you make a **deliberate** change to output format:

```bash
python3 tests/run_tests.py --update-snapshots
```

This overwrites the golden files. Always:
1. Review the git diff of every changed fixture file.
2. Verify the changes are what you intended.
3. Commit the updated snapshots together with the code change.

> **Never** update snapshots silently as part of an unrelated change. A snapshot
> change is a contract change.

### Adding a new snapshot

1. Add a new test method to `tests/regression/test_snapshot_expansion.py`
   following the existing pattern.
2. Run `python3 tests/run_tests.py --update-snapshots` to generate the fixture.
3. Run `python3 tests/run_tests.py --verbose` to confirm the new test passes.
4. Commit both the test and the fixture file.

---

## YAML Integrity Check

```bash
python3 tests/run_tests.py --yaml-check
```

This standalone check validates `data/boards.yaml` without running any test:

- Top-level keys (`boards`, `mcu_firmware`) must be present.
- Every `boards[]` entry must have `mcu`, `search_terms`, and `bltouch`.
- Every `mcu_firmware[]` entry must have `pattern` and `arch`.
- No generic pattern may shadow a more specific pattern that appears later
  (precedence validation).

Exit code 0 = valid, exit code 1 = errors found with details printed.

---

## Full Klipper Sweep

```bash
python3 tests/run_tests.py --full-klipper-sweep
```

The sweep:
1. Clones the Klipper repository with `--depth 1 --sparse` (config/ only).
2. Iterates every `generic-*.cfg` and `printer-*.cfg`.
3. Runs `parse_config()` + `extract_profile_defaults()` on each.
4. Classifies the result:

| Code | Meaning |
|------|---------|
| `PASS` | Full parse + extraction succeeded |
| `SAFE_ABORT` | TODO placeholder pins found — known graceful limitation |
| `UNSUPPORTED` | Experimental/unsupported sections present |
| `FAILURE` | Unhandled Python exception — requires investigation |

5. Prints a final statistics table.
6. Exits with code 1 if any `FAILURE` results were recorded.

The sweep requires `git` on `PATH` and network access. It runs automatically
on every push to `main` via GitHub Actions, but is skipped on PRs to keep
contributor iteration fast.

---

## CI Pipeline Overview

The GitHub Actions workflow in `.github/workflows/ci.yml` runs on every push to
`main` and every pull request.

```
push / PR
    │
    ├── lint              — python -m py_compile (syntax check all .py files)
    │
    ├── unit-tests        — runs full test suite (21 tests)
    │
    ├── yaml-integrity    — boards.yaml schema + precedence check
    │
    ├── regression-tests  — snapshot comparison (blocks merge on diff)
    │       └── needs: [unit-tests, yaml-integrity]
    │
    └── full-klipper-sweep  (push to main ONLY)
            └── needs: regression-tests
```

All jobs use `concurrency` cancellation — if you push multiple commits quickly
to the same PR, older CI runs cancel automatically.

### Blocking rules

Merges to `main` are blocked if any of the following jobs fail:
- `lint`
- `unit-tests`
- `yaml-integrity`
- `regression-tests`

The `full-klipper-sweep` is informational on main (does not block PRs).

---

## Zero-Dependency Design

The test runner uses only Python standard library modules:

```
unittest, sys, os, time, argparse, subprocess, tempfile, re
```

This means the tests can run on a Raspberry Pi Zero 2W with no pip installs
beyond the project's own `requirements.txt`. The full suite completes in
under 0.5 seconds on typical hardware.
