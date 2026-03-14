import glob
import re
import os
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
    ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#ffffff bg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # selected choice in checkbox prompts
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # help text for the user
    ('text', ''),                       # any generic text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
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
    print("\033[95m>>> Starting Hardware Discovery...\033[0m")
    mcu_path = discover_mcu()
    
    print("\033[95m>>> Fetching board database...\033[0m")
    boards = fetch_config_list()
    
    board = None
    match = re.search(r'usb-Klipper_([a-zA-Z0-9]+)_', mcu_path)
    if match:
        mcu = match.group(1).lower()
        print(f"\nDetected MCU: {mcu.upper()}\n")
        if mcu in MCU_SEARCH_TERMS:
            search_terms = MCU_SEARCH_TERMS[mcu]
            suggested_configs = []
            for b in boards:
                if any(term in b.lower() for term in search_terms):
                    suggested_configs.append(b)
            
            if suggested_configs:
                choices = suggested_configs + ["Search manually..."]
                choice = questionary.select(
                    "Suggested boards based on your MCU:",
                    choices=choices,
                    style=custom_style
                ).ask()
                
                if choice != "Search manually...":
                    board = choice
            else:
                print("No exact config matches found for suggestions. Please search manually.\n")
                
    if not board:
        board = questionary.autocomplete(
            "Select your board (type to search):",
            choices=boards,
            style=custom_style
        ).ask()
    
    kinematics = questionary.select(
        "Select Kinematics:",
        choices=["cartesian", "corexy", "delta"],
        style=custom_style
    ).ask()
    
    x_size = questionary.text("Enter X build volume (mm):", default="235", style=custom_style).ask()
    y_size = questionary.text("Enter Y build volume (mm):", default="235", style=custom_style).ask()
    z_size = questionary.text("Enter Z build volume (mm):", default="250", style=custom_style).ask()
    
    probe = questionary.select(
        "Select Probe Type:",
        choices=["None", "BLTouch", "Inductive", "CR-Touch"],
        style=custom_style
    ).ask()

    driver_type = questionary.select(
        "Select Stepper Driver Type:",
        choices=["None (Standard)", "TMC2208", "TMC2209", "TMC2130", "A4988"],
        style=custom_style
    ).ask()

    driver_mode = "Standalone"
    if driver_type in ["TMC2208", "TMC2209", "TMC2130"]:
        driver_mode = questionary.select(
            f"Select {driver_type} Communication Mode:",
            choices=["UART", "SPI", "Standalone"],
            style=custom_style
        ).ask()
    
    z_motors = questionary.select(
        "How many Z motors are you using?",
        choices=["1", "2"],
        style=custom_style
    ).ask()
    
    deploy_choice = questionary.select(
        "What would you like to do with the generated printer.cfg?",
        choices=[
            "Save locally (current directory)",
            "Deploy to Klipper host via SSH",
            "Start a temporary web server to download to PC"
        ],
        style=custom_style
    ).ask()
    
    ssh_data = {}
    if deploy_choice == "Deploy to Klipper host via SSH":
        default_host = "192.168.1.100"
        ssh_conn = os.environ.get('SSH_CONNECTION')
        if ssh_conn:
            parts = ssh_conn.split()
            if len(parts) >= 3:
                default_host = parts[2]
                
        ssh_data['host'] = questionary.text("SSH Host (IP or hostname):", default=default_host, style=custom_style).ask()
        ssh_data['user'] = questionary.text("SSH Username:", default="pi", style=custom_style).ask()
        ssh_data['password'] = questionary.password("SSH Password:", style=custom_style).ask()
        ssh_data['dest_path'] = questionary.text("Destination path on host:", default="~/printer_data/config/printer.cfg", style=custom_style).ask()

    return {
        "mcu_path": mcu_path,
        "board": board,
        "kinematics": kinematics,
        "x_size": x_size,
        "y_size": y_size,
        "z_size": z_size,
        "z_motors": z_motors,
        "probe": probe,
        "driver_type": driver_type,
        "driver_mode": driver_mode,
        "deploy_choice": deploy_choice,
        **ssh_data
    }
