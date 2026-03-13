import glob
import questionary
from .scraper import fetch_config_list

def discover_mcu():
    """Milestone 3: Auto-Discovery of MCU"""
    ports = glob.glob('/dev/serial/by-id/*')
    if not ports:
        return questionary.text("No serial devices found. Enter MCU path manually (e.g., /dev/ttyUSB0):").ask()
    
    choices = ports + ["Enter manually..."]
    choice = questionary.select("Select MCU serial port:", choices=choices).ask()
    if choice == "Enter manually...":
        return questionary.text("Enter MCU path manually:").ask()
    return choice

def run_wizard():
    """Runs the interactive CLI wizard to gather user preferences."""
    print("Discovering MCU...")
    mcu_path = discover_mcu()
    
    print("Fetching available boards from Klipper GitHub...")
    boards = fetch_config_list()
    
    board = questionary.autocomplete(
        "Select your board (type to search):",
        choices=boards
    ).ask()
    
    kinematics = questionary.select(
        "Select Kinematics:",
        choices=["cartesian", "corexy", "delta"]
    ).ask()
    
    x_size = questionary.text("Enter X build volume (mm):", default="235").ask()
    y_size = questionary.text("Enter Y build volume (mm):", default="235").ask()
    z_size = questionary.text("Enter Z build volume (mm):", default="250").ask()
    
    probe = questionary.select(
        "Select Probe Type:",
        choices=["None", "BLTouch", "Inductive", "CR-Touch"]
    ).ask()
    
    deploy_ssh = questionary.confirm("Deploy printer.cfg to Klipper host via SSH?").ask()
    ssh_data = {}
    if deploy_ssh:
        ssh_data['host'] = questionary.text("SSH Host (IP or hostname):", default="192.168.1.100").ask()
        ssh_data['user'] = questionary.text("SSH Username:", default="pi").ask()
        ssh_data['password'] = questionary.password("SSH Password:").ask()
        ssh_data['dest_path'] = questionary.text("Destination path on host:", default="~/printer_data/config/printer.cfg").ask()

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
