import glob
import re
import os
import sys
import questionary
from questionary import Style
from .scraper import fetch_config_list

MCU_SEARCH_TERMS = {
    "lpc1769": ["skr-v1.4", "skr-v1.3", "sgen-l"],
    "stm32f103": ["creality-v4.2.2", "creality-v4.2.7", "skr-mini-e3"],
    "stm32f446": ["octopus", "spider"],
    "rp2040": ["skr-pico"],
    "atmega2560": ["ramps", "mega2560"]
}

# Custom KIAUH-inspired style
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#4caf50 bold'),      # submitted answer text behind the question (green after selected)
    ('pointer', 'fg:#f44336 bold'),     # pointer used in select and checkbox prompts (red while selecting)
    ('highlighted', 'fg:#f44336 bold'), # pointed-at choice in select and checkbox prompts (red while selecting)
    ('selected', 'fg:#4caf50'),         # selected choice in checkbox prompts
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # help text for the user
    ('text', ''),                       # any generic text
    ('disabled', 'fg:#858585 italic'),  # disabled choices for select and checkbox prompts
    ('completion-menu', 'bg:#000000 fg:#ffffff'),
    ('completion-menu.completion.current', 'bg:#4caf50 fg:#000000')
])

def discover_mcu():
    """Milestone 3: Auto-Discovery of MCU"""
    ports = glob.glob('/dev/serial/by-id/*')
    if not ports:
        return questionary.text("No serial devices found. Enter MCU path manually (e.g., /dev/ttyUSB0):", style=custom_style).ask()
    
    choices = ports + ["Enter manually..."]
    choice = questionary.select("Select MCU serial port:", choices=choices, style=custom_style).ask()
    if choice == "Enter manually...":
        return questionary.text("Enter MCU path manually:", style=custom_style).ask()
    return choice

def run_wizard():
    """Runs the interactive CLI wizard to gather user preferences."""
    print("\033[96m>>> Starting Hardware Discovery...\033[0m")
    mcu_path = discover_mcu()
    
    print("\033[96m>>> Fetching board database...\033[0m")
    boards = fetch_config_list()
    
    suggested_configs = []
    match = re.search(r'usb-Klipper_([a-zA-Z0-9]+)_', mcu_path)
    if match:
        mcu = match.group(1).lower()
        print(f"\nDetected MCU: {mcu.upper()}\n")
        if mcu in MCU_SEARCH_TERMS:
            search_terms = MCU_SEARCH_TERMS[mcu]
            for b in boards:
                if any(term in b.lower() for term in search_terms):
                    suggested_configs.append(b)

    user_data = {
        "mcu_path": mcu_path,
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
