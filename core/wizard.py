import glob
import questionary
from questionary import Style
from .scraper import fetch_config_list

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
    
    deploy_ssh = questionary.confirm("Deploy printer.cfg to Klipper host via SSH?", style=custom_style).ask()
    ssh_data = {}
    if deploy_ssh:
        ssh_data['host'] = questionary.text("SSH Host (IP or hostname):", default="192.168.1.100", style=custom_style).ask()
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
        "probe": probe,
        "deploy_ssh": deploy_ssh,
        **ssh_data
    }
