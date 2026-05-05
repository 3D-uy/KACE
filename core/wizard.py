import glob
import re
import os
import sys
import questionary
from questionary import Style
from .scraper import fetch_config_list
from firmware.detector import discover_mcu_hardware
from core.style import custom_style

MCU_SEARCH_TERMS = {
    "lpc1769": ["skr-v1.4", "skr-v1.3", "sgen-l"],
    "stm32f103": ["creality-v4.2.2", "creality-v4.2.7", "skr-mini-e3"],
    "stm32f446": ["octopus", "spider"],
    "rp2040": ["skr-pico"],
    "atmega2560": ["ramps", "mega2560"]
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
    
    suggested_configs = []
    if detected_mcu:
        print(f"\nDetected MCU: {detected_mcu.upper()}\n")
        if detected_mcu in MCU_SEARCH_TERMS:
            search_terms = MCU_SEARCH_TERMS[detected_mcu]
            for b in boards:
                if any(term in b.lower() for term in search_terms):
                    suggested_configs.append(b)

    # Prompt user for manual config board finding if not completely derived
    if mcu_hint == "manual" and not detected_mcu:
        print(f"\nUsing manual MCU. You will have a chance to enter the compiler configuration later.")

    user_data = {
        "mcu_path": mcu_path,
        "mcu_type": detected_mcu,
        "mcu_hint": mcu_hint,
        "language": "English",
        "board": None,
        "kinematics": None,
        "x_size": "235",
        "y_size": "235",
        "z_size": "250",
        "probe": None,
        "driver_type": None,
        "driver_mode": "Standalone",
        "z_motors": None,
        "web_interface": None
    }
    
    step = 0
    while step < 11:
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
            ans = None
            if suggested_configs and not user_data["board"]:
                choices = suggested_configs + ["Search manually...", "Back", "Quit"]
                ans = questionary.select(
                    "Suggested boards based on your MCU:",
                    choices=choices,
                    style=custom_style
                ).ask()
                
                if ans == "Quit" or ans is None: sys.exit(0)
                if ans == "Back":
                    step -= 1
                    continue
                if ans != "Search manually...":
                    user_data["board"] = ans
                    step += 1
                    continue

            # Manually searching
            ans = questionary.autocomplete(
                "Select your board (type to search) [Ctrl+C to go back]:",
                choices=boards,
                style=custom_style
            ).ask()
            if ans is None:
                user_data["board"] = None
                if not suggested_configs:
                    step -= 1
                continue
            user_data["board"] = ans
            step += 1

        elif step == 2:
            ans = questionary.select(
                "Select Kinematics:",
                choices=["cartesian", "corexy", "delta", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                user_data["board"] = None
                step -= 1
                continue
            user_data["kinematics"] = ans
            step += 1

        elif step == 3:
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

        elif step == 4:
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

        elif step == 5:
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

        elif step == 6:
            ans = questionary.select(
                "Select Probe Type:",
                choices=["None", "BLTouch", "Inductive", "CR-Touch", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["probe"] = ans
            step += 1

        elif step == 7:
            ans = questionary.select(
                "Select Stepper Driver Type:",
                choices=["None (Standard)", "TMC2208", "TMC2209", "TMC2130", "A4988", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["driver_type"] = ans
            if ans in ["None (Standard)", "A4988"]:
                user_data["driver_mode"] = "Standalone"
                step += 2
            else:
                step += 1

        elif step == 8:
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

        elif step == 9:
            ans = questionary.select(
                "How many Z motors are you using?",
                choices=["1", "2", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                if user_data["driver_type"] in ["None (Standard)", "A4988"]:
                    step -= 2
                else:
                    step -= 1
                continue
            user_data["z_motors"] = ans
            step += 1

        elif step == 10:
            ans = questionary.select(
                "Select your Web Interface (for includes):",
                choices=["Mainsail", "Fluidd", "None", "Back", "Quit"],
                style=custom_style
            ).ask()
            if ans == "Quit" or ans is None: sys.exit(0)
            if ans == "Back":
                step -= 1
                continue
            user_data["web_interface"] = ans
            step += 1

    return user_data
