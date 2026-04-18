import sys
import questionary
from .scraper import fetch_config_list, fetch_raw_config, parse_config, extract_profile_defaults
from firmware.detector import discover_mcu_hardware
from core.style import custom_style
from data.profiles import THERMISTOR_PRESETS

MCU_SEARCH_TERMS = {
    "lpc1769": ["skr-v1.4", "skr-v1.3", "sgen-l"],
    "lpc1768": ["mks-sgenl", "sbase"],
    "stm32f103": ["creality-v4.2.2", "creality-v4.2.7", "skr-mini-e3"],
    "stm32f407": ["mks-robin-nano-v3", "skr-pro"],
    "stm32f429": ["skr-2", "octopus-pro-v1.0"],
    "stm32f446": ["octopus", "spider"],
    "stm32g0b1": ["manta", "skr-mini-e3-v3.0"],
    "stm32h723": ["octopus-max-ez"],
    "stm32f042": ["cheetah-v2.0"],
    "rp2040": ["skr-pico"],
    "atmega2560": ["ramps", "mega2560"],
    "atmega1284p": ["melzi"],
    "at90usb1286": ["printrboard"],
    "sam4e8e": ["duet2"],
    "samd51": ["duet3-mini"]
}

def discover_mcu():
    """Milestone 3: Auto-Discovery of MCU"""
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
        if detected_mcu in MCU_SEARCH_TERMS:
            search_terms = MCU_SEARCH_TERMS[detected_mcu]
            for b in board_configs:
                if any(term in b.lower() for term in search_terms):
                    suggested_configs.append(b)

    if mcu_hint == "manual" and not detected_mcu:
        print("\nUsing manual MCU. You will have a chance to enter the compiler configuration later.")

    user_data = {
        "mcu_path": mcu_path,
        "mcu_type": detected_mcu,
        "mcu_hint": mcu_hint,
        "language": "English",
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
    while step < 14:
        if step == 0:
            ans = questionary.select(
                "Select language for comments / Seleccione el idioma / Selecione o idioma:",
                choices=["English", "Español", "Português", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            user_data["language"] = ans
            step += 1

        elif step == 1:
            choices = ["Custom / Scratch Build"] + printer_configs
            ans = questionary.autocomplete(
                "Select your Printer Model (type to search) [Ctrl+C to go back]:",
                choices=choices,
                style=custom_style
            ).ask()
            
            if ans is None:
                step -= 1
                continue
                
            user_data["printer_profile"] = ans
            if ans != "Custom / Scratch Build":
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

        elif step == 2:
            choices = []
            if user_data["printer_profile"] != "Custom / Scratch Build":
                choices.append("Stock Board (from printer profile)")
                
            if suggested_configs and not user_data["board"]:
                choices.extend(suggested_configs)
                
            choices.extend(["Search manually...", "Back", "Quit"])
            
            ans = questionary.select(
                "Select your Board:",
                choices=choices,
                style=custom_style
            ).ask()
            
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
                
            if ans == "Stock Board (from printer profile)":
                user_data["board"] = user_data["printer_profile"]
                step += 1
                continue
                
            if ans != "Search manually...":
                user_data["board"] = ans
                step += 1
                continue

            ans = questionary.autocomplete(
                "Select your board manually (type to search) [Ctrl+C to go back]:",
                choices=board_configs,
                style=custom_style
            ).ask()
            if ans is None:
                continue
                
            user_data["board"] = ans
            step += 1

        elif step == 3:
            ans = questionary.select(
                "Select Kinematics:",
                choices=["cartesian", "corexy", "delta", "Back", "Quit"],
                default=user_data["kinematics"] if user_data["kinematics"] in ["cartesian", "corexy", "delta"] else None,
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["kinematics"] = ans
            step += 1

        elif step == 4:
            ans = questionary.text(
                "Enter X build volume (mm) [Ctrl+C to go back]:", 
                default=user_data["x_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["x_size"] = ans
            step += 1

        elif step == 5:
            ans = questionary.text(
                "Enter Y build volume (mm) [Ctrl+C to go back]:", 
                default=user_data["y_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["y_size"] = ans
            step += 1

        elif step == 6:
            ans = questionary.text(
                "Enter Z build volume (mm) [Ctrl+C to go back]:", 
                default=user_data["z_size"], 
                style=custom_style
            ).ask()
            if ans is None:
                step -= 1
                continue
            user_data["z_size"] = ans
            step += 1

        elif step == 7:
            ans = questionary.select(
                "Select Probe Type:",
                choices=["None", "BLTouch", "Inductive", "CR-Touch", "Back", "Quit"],
                default=user_data["probe"] if user_data["probe"] in ["None", "BLTouch", "Inductive", "CR-Touch"] else None,
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["probe"] = ans
            step += 1

        elif step == 8:
            preset_choices = list(THERMISTOR_PRESETS)
            if user_data["hotend_thermistor"] not in preset_choices:
                preset_choices.insert(0, user_data["hotend_thermistor"])
            choices = preset_choices + ["Other (Manual Entry)", "Back", "Quit"]
            
            ans = questionary.select(
                "Select Hotend Thermistor:",
                choices=choices,
                default=user_data["hotend_thermistor"] if user_data["hotend_thermistor"] in choices else None,
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            if ans == "Other (Manual Entry)":
                manual_ans = questionary.text("Enter custom hotend thermistor name:", style=custom_style).ask()
                if manual_ans is None:
                    continue
                user_data["hotend_thermistor"] = manual_ans
            else:
                user_data["hotend_thermistor"] = ans
            step += 1
            
        elif step == 9:
            preset_choices = list(THERMISTOR_PRESETS)
            if user_data["bed_thermistor"] not in preset_choices:
                preset_choices.insert(0, user_data["bed_thermistor"])
            choices = preset_choices + ["Other (Manual Entry)", "Back", "Quit"]
            
            ans = questionary.select(
                "Select Bed Thermistor:",
                choices=choices,
                default=user_data["bed_thermistor"] if user_data["bed_thermistor"] in choices else None,
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            if ans == "Other (Manual Entry)":
                manual_ans = questionary.text("Enter custom bed thermistor name:", style=custom_style).ask()
                if manual_ans is None:
                    continue
                user_data["bed_thermistor"] = manual_ans
            else:
                user_data["bed_thermistor"] = ans
            step += 1

        elif step == 10:
            ans = questionary.select(
                "Select Stepper Driver Type:",
                choices=["None (Standard)", "TMC2208", "TMC2209", "TMC2225", "TMC2130", "TMC5160", "A4988", "DRV8825", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["driver_type"] = ans
            if ans in ["None (Standard)", "A4988", "DRV8825"]:
                user_data["driver_mode"] = "Standalone"
                step += 2
            else:
                step += 1

        elif step == 11:
            ans = questionary.select(
                f"Select {user_data['driver_type']} Communication Mode:",
                choices=["UART", "SPI", "Standalone", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["driver_mode"] = ans
            step += 1

        elif step == 12:
            ans = questionary.select(
                "Select your Web Interface (for includes):",
                choices=["Mainsail", "Fluidd", "None", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                if user_data["driver_type"] in ["None (Standard)", "A4988", "DRV8825"]:
                    step -= 2
                else:
                    step -= 1
                continue
            user_data["web_interface"] = ans
            step += 1

        elif step == 13:
            ans = questionary.select(
                "How many Z motors are you using?",
                choices=["1", "2", "3", "4", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["z_motors"] = ans
            step += 1

    return user_data
