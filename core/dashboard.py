# core/dashboard.py
#
# System landing dashboard for KACE.
# Detects the state of the local Klipper ecosystem and presents
# a top-level action menu before entering any workflow.
#
# Design principles:
#   - detect_system_state() is fast, read-only, no network calls.
#   - Detection paths use KIAUH/MainsailOS defaults; constants are
#     defined at module level so they can be made configurable later.
#   - All user-facing strings go through t() from core.translations.
#   - Bypassed entirely by kace.py when CI/auto/dev env vars are set.

import os
import subprocess
import sys

import questionary

from core.style import custom_style
from core.translations import t
from core.banner import print_kace_banner

# ── Detection path constants (KIAUH / MainsailOS defaults) ────
# Centralised here so future configurability is one-line change.
_PATH_KLIPPER     = os.path.expanduser("~/klipper")
_PATH_MOONRAKER   = os.path.expanduser("~/moonraker")
_PATH_MAINSAIL    = os.path.expanduser("~/mainsail")
_PATH_FLUIDD      = os.path.expanduser("~/fluidd")
_PATH_PRINTER_CFG = os.path.expanduser("~/printer_data/config/printer.cfg")

# ── ANSI helpers ───────────────────────────────────────────────
_G = "\033[92m"   # green
_Y = "\033[93m"   # yellow
_C = "\033[96m"   # cyan
_B = "\033[1m"    # bold
_R = "\033[0m"    # reset
_DIM = "\033[2m"  # dim

_OK  = f"{_G}✅{_R}"
_NOK = f"{_Y}❌{_R}"


def _service_active(name: str) -> bool:
    """Return True if a systemd service is active (Linux only)."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", name],
            timeout=3,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def detect_system_state() -> dict:
    """Probe the local system for Klipper ecosystem components.

    Returns a dict with boolean presence flags and detected MCU string.
    Detection is fast, read-only, and safe to call on any platform.
    """
    klipper   = os.path.isdir(_PATH_KLIPPER)   or _service_active("klipper")
    moonraker = os.path.isdir(_PATH_MOONRAKER)  or _service_active("moonraker")
    mainsail  = os.path.isdir(_PATH_MAINSAIL)
    fluidd    = os.path.isdir(_PATH_FLUIDD)
    has_cfg   = os.path.isfile(_PATH_PRINTER_CFG)

    # Reuse the existing MCU detector — returns empty dict on failure.
    mcu = None
    mcu_path = None
    try:
        from firmware.detector import discover_mcu_hardware
        ctx = discover_mcu_hardware(interactive=False)
        mcu = ctx.get("derived_mcu")
        mcu_path = ctx.get("mcu_path")
    except Exception:
        pass

    return {
        "klipper":     klipper,
        "moonraker":   moonraker,
        "mainsail":    mainsail,
        "fluidd":      fluidd,
        "printer_cfg": has_cfg,
        "mcu":         mcu,
        "mcu_path":    mcu_path,
    }


def get_suggestions(state: dict) -> list:
    """Return a list of translated suggestion strings based on system state.

    Purely informational — no actions are taken here.
    """
    suggestions = []
    if not state["klipper"]:
        suggestions.append(t("dashboard.suggest_no_klipper"))
    if not state["moonraker"]:
        suggestions.append(t("dashboard.suggest_no_moonraker"))
    if not state["mainsail"] and not state["fluidd"]:
        suggestions.append(t("dashboard.suggest_no_webui"))
    if not state["printer_cfg"]:
        suggestions.append(t("dashboard.suggest_no_cfg"))
    return suggestions


def _render_status_panel(state: dict) -> None:
    """Print the colored system status table."""
    title = t("dashboard.status_title")
    
    # Pre-calculate MCU text to determine dynamic width
    mcu_val = state.get("mcu")
    mcu_path = state.get("mcu_path")
    
    if mcu_val:
        mcu_raw = f"{mcu_val} ({t('dashboard.detected')})"
        mcu_text = f"{mcu_val} {_DIM}({t('dashboard.detected')}){_R}"
    elif mcu_path:
        base_path = mcu_path.split('/')[-1]
        mcu_raw = f"{base_path}"
        mcu_text = f"{base_path}"
    else:
        mcu_raw = t("dashboard.no_mcu")
        mcu_text = f"{_DIM}{mcu_raw}{_R}"

    # Calculate dynamic width (minimum 42, expand if MCU path is long)
    width = max(42, 14 + 1 + len(mcu_raw) + 2)
    border = "─" * width

    def _row(label: str, ok: bool, detail: str) -> str:
        icon = _OK if ok else _NOK
        status = t("dashboard.installed") if ok else t("dashboard.not_found")
        return f"  │  {_B}{label:<14}{_R} {icon}  {status:<{width - 19}}│"

    print(f"\n  {_C}┌─ {_B}{title}{_R}{_C} {border[:width - len(title) - 3]}┐{_R}")
    print(_row("Klipper",    state["klipper"],     ""))
    print(_row("Moonraker",  state["moonraker"],   ""))
    print(_row("Mainsail",   state["mainsail"],    ""))
    print(_row("Fluidd",     state["fluidd"],      ""))

    # printer.cfg row
    cfg_ok     = state["printer_cfg"]
    cfg_icon   = _OK if cfg_ok else _NOK
    cfg_status = t("dashboard.found") if cfg_ok else t("dashboard.not_found")
    print(f"  │  {_B}{'printer.cfg':<14}{_R} {cfg_icon}  {cfg_status:<{width - 19}}│")

    pad_len = max(0, width - 16 - len(mcu_raw))
    mcu_padded = mcu_text + (" " * pad_len)
    
    print(f"  │  {_B}{'MCU':<14}{_R} {mcu_padded}│")

    print(f"  {_C}└{'─' * (width + 2)}┘{_R}")


def _render_suggestions(suggestions: list) -> None:
    """Print suggestion lines below the status panel."""
    if not suggestions:
        return
    print(f"\n  {_Y}{_B}💡 {t('dashboard.suggestions_header')}:{_R}")
    for s in suggestions[:4]:   # cap at 4 to keep it tidy
        print(f"  {_Y}  • {s}{_R}")


def _show_manage_view(state: dict) -> None:
    """Print the full component status view and wait for user input."""
    title = t("dashboard.manage_header")
    print(f"\n  {_C}{_B}{title}{_R}")
    _render_status_panel(state)
    suggestions = get_suggestions(state)
    _render_suggestions(suggestions)
    print(f"\n  {_DIM}{t('dashboard.press_enter')}{_R}")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass


def run_dashboard(state: dict) -> str:
    """Display the KACE landing dashboard and return the chosen action.

    Returns one of: "generate", "reconfigure", "manage", "quit".
    The "manage" case is handled entirely inside this function's loop
    (it shows the status view and loops back to the menu), so callers
    only ever receive "generate", "reconfigure", or "quit".
    """
    while True:
        # Redraw banner + status on every loop iteration so the screen
        # stays fresh after returning from the manage view.
        print_kace_banner("Klipper Automated Configuration Ecosystem")

        _render_status_panel(state)
        suggestions = get_suggestions(state)
        _render_suggestions(suggestions)
        print("")

        choices = [
            {"name": t("dashboard.action_generate"),  "value": "generate"},
            {"name": t("dashboard.action_reconfig"),  "value": "reconfigure"},
            {"name": t("dashboard.action_manage"),    "value": "manage"},
            {"name": t("dashboard.action_quit"),      "value": "quit"},
        ]

        try:
            action = questionary.select(
                t("dashboard.action_prompt"),
                choices=choices,
                style=custom_style,
            ).ask()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        if action is None or action == "quit":
            return "quit"

        if action == "manage":
            _show_manage_view(state)
            continue    # loop back to redraw dashboard

        # "generate" or "reconfigure" — return to kace.py
        return action
