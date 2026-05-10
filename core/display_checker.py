# core/display_checker.py
#
# Display Compatibility Layer — KACE
#
# Detects display-related sections in a parsed Klipper config, looks up
# their compatibility status from data/displays.yaml, and returns structured
# findings for the warning system in kace.py.
#
# Public API:
#   check_display_compatibility(parsed_cfg, printer_filename, board_filename)
#       → list[dict]  — list of findings, empty if no display sections found
#
# Each finding dict:
#   {
#     "section":        str   — Klipper section name (e.g. "t5uid1")
#     "status":         str   — "supported" | "partial" | "unsupported" | "untested"
#     "recommendation": str   — "disconnect" | "optional" | "none" | ""
#     "notes":          list  — human-readable bullet points
#     "source":         str   — "printer_profile" | "display_config" | "fallback"
#   }
#
# Design contract:
#   - Works without data/displays.yaml (hardcoded fallback dict)
#   - Never modifies the parsed config
#   - Never raises exceptions to the caller

import os

# ── Known display section names ────────────────────────────────────────────────
# All Klipper config section names that indicate a display-related component.
# Used to filter parsed config keys before database lookup.
_DISPLAY_SECTION_NAMES = {
    # Native Klipper display sections
    "display", "lcd_menu", "display_status", "display_template", "display_data",
    "hd44780", "ssd1306", "uc1701", "st7920",
    # OEM / proprietary protocols
    "t5uid1", "dwin_set", "tft_serial",
    # LED / exotic
    "neopixel", "dotstar", "sx1509",
}

# ── Hardcoded fallback ────────────────────────────────────────────────────────
# Used when data/displays.yaml is missing (e.g., sparse clone without data/).
# Mirrors the critical entries from displays.yaml.
# format: section_name → {status, recommendation, notes}

_DISPLAY_CONFIGS_FALLBACK = {
    "display": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["Standard LCD displays are natively supported by Klipper"],
    },
    "lcd_menu": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["lcd_menu is a native Klipper feature — fully supported"],
    },
    "display_status": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["display_status is a standard Klipper object — no compatibility concerns"],
    },
    "display_template": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["display_template is a native Klipper feature — fully supported"],
    },
    "display_data": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["display_data is a native Klipper feature — fully supported"],
    },
    "t5uid1": {
        "status": "unsupported",
        "recommendation": "disconnect",
        "notes": [
            "OEM DGUS touchscreen protocol — designed for Creality Marlin firmware",
            "No built-in Klipper support without community plugins",
            "Expected outcome: black screen or boot loop",
        ],
    },
    "dwin_set": {
        "status": "partial",
        "recommendation": "disconnect",
        "notes": [
            "DWIN displays require firmware matching the display version",
            "Community plugins exist but are not installed by KACE",
            "Mismatch causes: frozen UI, missing menus, or black screen",
        ],
    },
    "tft_serial": {
        "status": "partial",
        "recommendation": "optional",
        "notes": [
            "Serial TFT displays use a bridge protocol designed for Marlin",
            "Menu functionality is typically limited or absent under Klipper",
            "Web UI (Mainsail/Fluidd) provides full feature parity",
        ],
    },
    "neopixel": {
        "status": "unsupported",
        "recommendation": "none",
        "notes": ["Neopixel/WS2812 LED sections are outside KACE's current scope"],
    },
    "dotstar": {
        "status": "unsupported",
        "recommendation": "none",
        "notes": ["Dotstar/APA102 LED sections are outside KACE's current scope"],
    },
    "sx1509": {
        "status": "unsupported",
        "recommendation": "none",
        "notes": ["SX1509 GPIO expander is not supported by KACE's configuration engine"],
    },
    "hd44780": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["HD44780 character displays are natively supported by Klipper"],
    },
    "ssd1306": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["SSD1306 OLED displays are natively supported by Klipper"],
    },
    "uc1701": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["UC1701 displays (e.g., mini12864) are natively supported by Klipper"],
    },
    "st7920": {
        "status": "supported",
        "recommendation": "none",
        "notes": ["ST7920 displays are natively supported by Klipper"],
    },
}

_PRINTER_PROFILES_FALLBACK = {
    "cr6-se": {
        "display_type": "t5uid1",
        "status": "unsupported",
        "recommendation": "disconnect",
        "notes": [
            "The CR-6 SE uses a proprietary DGUS/t5uid1 touchscreen with Creality OEM firmware",
            "Not compatible with Klipper without a community firmware patch",
            "Recommended: disconnect display and use Mainsail or Fluidd web interface",
        ],
    },
    "artillery-sidewinder": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": [
            "Artillery Sidewinder uses a serial TFT display designed for Marlin",
            "Serial TFT menus are typically non-functional under Klipper",
            "Web UI (Mainsail/Fluidd) provides full printer control",
        ],
    },
    "artillery-genius": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": [
            "Artillery Genius uses a serial TFT display designed for Marlin",
            "Serial TFT menus are typically non-functional under Klipper",
        ],
    },
    "artillery-hornet": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": [
            "Artillery Hornet uses a serial TFT display designed for Marlin",
            "Serial TFT menus are typically non-functional under Klipper",
        ],
    },
    "cr10-smart": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": ["CR-10 Smart TFT display has limited functionality under Klipper"],
    },
    "ender-6": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": ["Ender 6 TFT display has limited compatibility with Klipper"],
    },
    "mks-robin": {
        "display_type": "tft_serial",
        "status": "partial",
        "recommendation": "optional",
        "notes": ["MKS TFT displays have limited compatibility with Klipper"],
    },
}


def _load_display_db() -> tuple[dict, dict]:
    """Load display compatibility data from data/displays.yaml.

    Returns a tuple of (display_configs_dict, printer_profiles_dict).
    Falls back to the hardcoded dicts above if the file is missing or unparseable.
    Guarantees zero regression risk — never raises.
    """
    try:
        import yaml
        _db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'displays.yaml')
        _db_path = os.path.normpath(_db_path)
        with open(_db_path, 'r', encoding='utf-8') as f:
            db = yaml.safe_load(f)

        display_configs = db.get('display_configs') or {}
        printer_profiles = db.get('printer_display_profiles') or {}

        # Validate we got real data — fall back per-dict if empty
        if not display_configs:
            display_configs = _DISPLAY_CONFIGS_FALLBACK
        if not printer_profiles:
            printer_profiles = _PRINTER_PROFILES_FALLBACK

        return display_configs, printer_profiles

    except Exception:
        return _DISPLAY_CONFIGS_FALLBACK, _PRINTER_PROFILES_FALLBACK


# Module-level cache — loaded once per process
_DISPLAY_CONFIGS, _PRINTER_PROFILES = _load_display_db()


def detect_display_sections(parsed_cfg: dict) -> list:
    """Return a list of display-related section names found in the parsed config.

    Checks only against the known set of display section names (_DISPLAY_SECTION_NAMES).
    Does NOT include auxiliary sections like 'display_status' that appear in
    virtually all configs — only genuine display hardware sections trigger a finding.
    """
    found = []
    for key in parsed_cfg:
        # Normalize: strip trailing specifiers like "neopixel my_led" → "neopixel"
        base_key = key.split()[0].lower()
        if base_key in _DISPLAY_SECTION_NAMES:
            if base_key not in found:
                found.append(base_key)
    return found


def _match_printer_profile(printer_filename: str) -> tuple[str, dict] | tuple[None, None]:
    """Try to match a printer filename against known printer display profiles.

    Returns (profile_key, profile_dict) on match, (None, None) if no match.
    Checked before display_configs — printer profile takes precedence.
    """
    fname_lower = printer_filename.lower()
    for profile_key, profile_data in _PRINTER_PROFILES.items():
        if profile_key in fname_lower:
            return profile_key, profile_data
    return None, None


def get_display_compat(section_name: str, printer_filename: str = "") -> dict | None:
    """Look up compatibility data for a single display section.

    Checks printer_display_profiles first (by filename), then display_configs
    (by section name). Returns None if no entry found (→ 'untested' at call site).

    Args:
        section_name:     Klipper config section name (e.g. "t5uid1")
        printer_filename: Optional printer profile filename for OEM matching

    Returns:
        dict with keys: status, recommendation, notes, source
        None if not found in either database.
    """
    # 1. Try printer profile match first (most specific)
    if printer_filename:
        profile_key, profile_data = _match_printer_profile(printer_filename)
        if profile_data:
            return {
                "status":         profile_data.get("status", "untested"),
                "recommendation": profile_data.get("recommendation", "none"),
                "notes":          profile_data.get("notes", []),
                "source":         "printer_profile",
            }

    # 2. Try section-based lookup
    section_lower = section_name.lower().split()[0]
    if section_lower in _DISPLAY_CONFIGS:
        entry = _DISPLAY_CONFIGS[section_lower]
        return {
            "status":         entry.get("status", "untested"),
            "recommendation": entry.get("recommendation", "none"),
            "notes":          entry.get("notes", []),
            "source":         "display_config",
        }

    return None


def check_display_compatibility(
    parsed_cfg: dict,
    printer_filename: str = "",
    board_filename:   str = "",
) -> list:
    """Main public entry point — check a parsed config for display compatibility issues.

    Steps:
    1. Try to match the printer model against printer_display_profiles (highest priority).
    2. Scan parsed config sections for known display section names.
    3. For each detected section, look up its status in display_configs.
    4. Unknown display sections are classified as 'untested'.
    5. Sections with status 'supported' are included but won't trigger a warning.

    Args:
        parsed_cfg:       Parsed config dict from core/scraper.parse_config()
        printer_filename: Printer profile filename (e.g. "printer-cr6-se.cfg")
        board_filename:   Board config filename (e.g. "generic-creality-v4.2.2.cfg")

    Returns:
        List of finding dicts. Empty list = no display sections detected.
        Each finding: {section, status, recommendation, notes, source}
    """
    findings = []
    seen_sections = set()

    # ── Step 1: Printer profile match (highest priority) ──────────────────────
    # If the printer model is known to have a problematic display, report it
    # even if the board config doesn't contain explicit display sections.
    if printer_filename:
        profile_key, profile_data = _match_printer_profile(printer_filename)
        if profile_data and profile_data.get("status") in ("partial", "unsupported"):
            display_type = profile_data.get("display_type", "tft_serial")
            findings.append({
                "section":         display_type,
                "status":          profile_data.get("status", "untested"),
                "recommendation":  profile_data.get("recommendation", "none"),
                "notes":           profile_data.get("notes", []),
                "source":          "printer_profile",
                "printer_profile": profile_key,
            })
            seen_sections.add(display_type)

    # ── Step 2: Scan config sections ──────────────────────────────────────────
    detected = detect_display_sections(parsed_cfg)

    for section in detected:
        if section in seen_sections:
            continue  # Already reported via printer profile

        # ── Step 3: Look up display_configs ───────────────────────────────────
        section_lower = section.lower()
        if section_lower in _DISPLAY_CONFIGS:
            entry = _DISPLAY_CONFIGS[section_lower]
            findings.append({
                "section":        section,
                "status":         entry.get("status", "untested"),
                "recommendation": entry.get("recommendation", "none"),
                "notes":          entry.get("notes", []),
                "source":         "display_config",
            })
        else:
            # ── Step 4: Unknown section → untested ────────────────────────────
            findings.append({
                "section":        section,
                "status":         "untested",
                "recommendation": "none",
                "notes":          [
                    f"Section '[{section}]' was detected but has no entry in KACE's display database.",
                    "Compatibility with Klipper is unknown.",
                ],
                "source":         "fallback",
            })

        seen_sections.add(section)

    return findings
