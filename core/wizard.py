import sys
import os
import questionary
from .scraper import fetch_config_list, fetch_raw_config, parse_config, extract_profile_defaults
from firmware.detector import discover_mcu_hardware
from core.style import custom_style
from data.profiles import THERMISTOR_PRESETS
from core.translations import t, get_lang

_BACK = "__back__"
_QUIT = "__quit__"

def _back_choice():
    return {"name": t("choice.back"), "value": _BACK}

def _quit_choice():
    return {"name": t("choice.quit"), "value": _QUIT}


# ── Hardware database ──────────────────────────────────────────────────────────
# Loaded from data/boards.yaml. The hardcoded dict below is the fallback used
# when the YAML file is missing (e.g., partial clone) or cannot be parsed.

_MCU_SEARCH_TERMS_FALLBACK = {
    "lpc1769":    ["skr-v1.4", "skr-v1.3", "sgen-l"],
    "lpc1768":    ["mks-sgenl", "sbase"],
    "stm32f103":  ["creality-v4.2.2", "creality-v4.2.7", "skr-mini-e3"],
    "stm32f407":  ["mks-robin-nano-v3", "skr-pro"],
    "stm32f429":  ["skr-2", "octopus-pro-v1.0"],
    "stm32f446":  ["octopus", "spider"],
    "stm32g0b1":  ["manta", "skr-mini-e3-v3.0"],
    "stm32h723":  ["octopus-max-ez"],
    "stm32f042":  ["cheetah-v2.0"],
    "rp2040":     ["skr-pico"],
    "atmega2560": ["ramps", "mega2560"],
    "atmega1284p":["melzi"],
    "at90usb1286":["printrboard"],
    "sam4e8e":    ["duet2"],
    "samd51":     ["duet3-mini"],
}

def _load_mcu_search_terms() -> dict:
    """Load MCU → board search terms from data/boards.yaml.

    Falls back to the hardcoded dict above if the file is missing
    or cannot be parsed — guarantees zero regression risk.
    """
    try:
        import yaml
        _db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'boards.yaml')
        _db_path = os.path.normpath(_db_path)
        with open(_db_path, 'r', encoding='utf-8') as f:
            db = yaml.safe_load(f)
        result = {}
        for entry in db.get('boards', []):
            mcu = entry.get('mcu')
            terms = entry.get('search_terms', [])
            if mcu and terms:
                result[mcu] = terms
        return result if result else _MCU_SEARCH_TERMS_FALLBACK
    except Exception:
        return _MCU_SEARCH_TERMS_FALLBACK

MCU_SEARCH_TERMS = _load_mcu_search_terms()


def discover_mcu():
    """Detect and return connected MCU hardware."""
    return discover_mcu_hardware()

def run_wizard():
    """Runs the interactive CLI wizard to gather user preferences."""
    print("\033[96m>>> Starting Hardware Discovery...\033[0m")
    mcu_context = discover_mcu()
    mcu_path = mcu_context.get("mcu_path")
    detected_mcu = mcu_context.get("derived_mcu")
    mcu_hint = mcu_context.get("hint")
    
    print("\033[96m>>> Fetching board database...\033[0m")
    boards = fetch_config_list()
    
    printer_configs = [b for b in boards if b.startswith("printer-")]
    board_configs = [b for b in boards if b.startswith("generic-")]
    
    suggested_configs = []
    if detected_mcu:
        print(f"\nDetected MCU: {detected_mcu.upper()}\n")
        
        matched_base_mcu = None
        for base_mcu in MCU_SEARCH_TERMS:
            if detected_mcu.startswith(base_mcu):
                matched_base_mcu = base_mcu
                break
                
        if matched_base_mcu:
            search_terms = MCU_SEARCH_TERMS[matched_base_mcu]
            for b in board_configs:
                if any(term in b.lower() for term in search_terms):
                    suggested_configs.append(b)

    if mcu_hint == "manual" and not detected_mcu:
        print("\nUsing manual MCU. You will have a chance to enter the compiler configuration later.")

    user_data = {
        "mcu_path": mcu_path,
        "mcu_type": detected_mcu,
        "mcu_hint": mcu_hint,
        # Sync from the live language state set by the dashboard language picker.
        # Falls back to "English" only in --auto / CI mode (dashboard bypassed).
        "language": get_lang(),
        "printer_profile": None,
        "board": None,
        "kinematics": "cartesian",
        "x_size": "235",
        "y_size": "235",
        "z_size": "250",
        "probe": "None",
        "hotend_thermistor": "EPCOS 100K B57560G104F",
        "bed_thermistor": "EPCOS 100K B57560G104F",
        "driver_type": None,
        "driver_mode": "Standalone",
        "z_motors": None,
        "web_interface": None
    }
    
    step = 0
    while step < 13:
        if step == 0:
            custom_choice_str = t("choice.custom_scratch")
            choices = [custom_choice_str] + printer_configs
            ans = questionary.autocomplete(
                t("wizard.select_printer_model"),
                choices=choices,
                style=custom_style
            ).ask()
            
            if ans is None:
                step -= 1
                continue
                
            user_data["printer_profile"] = "Custom / Scratch Build" if ans == custom_choice_str else ans
            
            if ans != custom_choice_str:
                print(f"\n\033[96m>>> Loading defaults for {ans}...\033[0m")
                raw = fetch_raw_config(ans)
                if raw:
                    parsed = parse_config(raw, ans)
                    defaults = extract_profile_defaults(parsed)
                    for k, v in defaults.items():
                        user_data[k] = v
                        
                    print("\n\033[92mDetected profile:\033[0m")
                    print(f"  - Build volume: {user_data.get('x_size')} x {user_data.get('y_size')} x {user_data.get('z_size')}")
                    print(f"  - Kinematics: {user_data.get('kinematics')}")
                    print(f"  - Thermistors: {user_data.get('hotend_thermistor')} (Hotend), {user_data.get('bed_thermistor')} (Bed)")
            step += 1

        elif step == 1:
            choices = []
            if user_data["printer_profile"] != "Custom / Scratch Build":
                choices.append({"name": t("choice.stock_board"), "value": "__stock__"})
                
            if suggested_configs and not user_data["board"]:
                choices.extend(suggested_configs)
                
            choices.extend([{"name": t("choice.search_manually"), "value": "__search__"}, _back_choice(), _quit_choice()])
            
            ans = questionary.select(
                t("wizard.select_board"),
                choices=choices,
                style=custom_style
            ).ask()
            
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
                
            if ans == "__stock__":
                user_data["board"] = user_data["printer_profile"]
                step += 1
                continue
                
            if ans != "__search__":
                user_data["board"] = ans
                step += 1
                continue

            ans = questionary.autocomplete(
                t("wizard.select_board_manual"),
                choices=board_configs,
                style=custom_style
            ).ask()
            if ans is None:
                continue
                
            user_data["board"] = ans
            step += 1

        elif step == 2:
            ans = questionary.select(
                t("wizard.select_kinematics"),
                choices=["cartesian", "corexy", "delta", _back_choice(), _quit_choice()],
                default=user_data["kinematics"] if user_data["kinematics"] in ["cartesian", "corexy", "delta"] else None,
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            user_data["kinematics"] = ans
            step += 1

        elif step == 3:
            ans = questionary.text(
                t("wizard.x_volume"), 
                default=user_data["x_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["x_size"] = ans
            step += 1

        elif step == 4:
            ans = questionary.text(
                t("wizard.y_volume"), 
                default=user_data["y_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["y_size"] = ans
            step += 1

        elif step == 5:
            ans = questionary.text(
                t("wizard.z_volume"), 
                default=user_data["z_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["z_size"] = ans
            step += 1

        elif step == 6:
            ans = questionary.select(
                t("wizard.select_probe"),
                choices=["None", "BLTouch", "Inductive", "CR-Touch", _back_choice(), _quit_choice()],
                default=user_data["probe"] if user_data["probe"] in ["None", "BLTouch", "Inductive", "CR-Touch"] else None,
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            user_data["probe"] = ans
            step += 1

        elif step == 7:
            preset_choices = list(THERMISTOR_PRESETS)
            if user_data["hotend_thermistor"] not in preset_choices:
                preset_choices.insert(0, user_data["hotend_thermistor"])
            choices = preset_choices + [{"name": t("choice.other_manual"), "value": "__other__"}, _back_choice(), _quit_choice()]
            
            ans = questionary.select(
                t("wizard.select_hotend_therm"),
                choices=choices,
                default=user_data["hotend_thermistor"] if user_data["hotend_thermistor"] in preset_choices else None,
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            if ans == "__other__":
                manual_ans = questionary.text(t("wizard.custom_hotend_therm"), style=custom_style).ask()
                if manual_ans is None:
                    continue
                user_data["hotend_thermistor"] = manual_ans
            else:
                user_data["hotend_thermistor"] = ans
            step += 1
            
        elif step == 8:
            preset_choices = list(THERMISTOR_PRESETS)
            if user_data["bed_thermistor"] not in preset_choices:
                preset_choices.insert(0, user_data["bed_thermistor"])
            choices = preset_choices + [{"name": t("choice.other_manual"), "value": "__other__"}, _back_choice(), _quit_choice()]
            
            ans = questionary.select(
                t("wizard.select_bed_therm"),
                choices=choices,
                default=user_data["bed_thermistor"] if user_data["bed_thermistor"] in preset_choices else None,
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            if ans == "__other__":
                manual_ans = questionary.text(t("wizard.custom_bed_therm"), style=custom_style).ask()
                if manual_ans is None:
                    continue
                user_data["bed_thermistor"] = manual_ans
            else:
                user_data["bed_thermistor"] = ans
            step += 1

        elif step == 9:
            ans = questionary.select(
                t("wizard.select_driver"),
                choices=["None (Standard)", "TMC2208", "TMC2209", "TMC2225", "TMC2130", "TMC5160", "A4988", "DRV8825", _back_choice(), _quit_choice()],
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            user_data["driver_type"] = ans
            if ans in ["None (Standard)", "A4988", "DRV8825"]:
                user_data["driver_mode"] = "Standalone"
                step += 2
            else:
                step += 1

        elif step == 10:
            ans = questionary.select(
                t("wizard.select_driver_mode", driver=user_data["driver_type"]),
                choices=["UART", "SPI", "Standalone", _back_choice(), _quit_choice()],
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            user_data["driver_mode"] = ans
            step += 1

        elif step == 11:
            ans = questionary.select(
                t("wizard.select_web_ui"),
                choices=["Mainsail", "Fluidd", "None", _back_choice(), _quit_choice()],
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                if user_data["driver_type"] in ["None (Standard)", "A4988", "DRV8825"]:
                    step -= 2
                else:
                    step -= 1
                continue
            user_data["web_interface"] = ans
            step += 1

        elif step == 12:
            ans = questionary.select(
                t("wizard.z_motors"),
                choices=["1", "2", "3", "4", _back_choice(), _quit_choice()],
                style=custom_style
            ).ask()
            if ans == _QUIT or ans is None: sys.exit(0)
            if ans == _BACK:
                step -= 1
                continue
            user_data["z_motors"] = ans
            step += 1

    return user_data
