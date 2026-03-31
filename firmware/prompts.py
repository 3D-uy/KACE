import questionary
from core.style import custom_style

def prompt_communication_interface(mcu):
    """
    Called when the derivation engine cannot confidently infer the comms interface.
    """
    ans = questionary.select(
        f"Select the communication interface for {mcu.upper()}:",
        choices=["USB", "UART", "CAN", "SPI"],
        style=custom_style
    ).ask()
    return ans

def prompt_bootloader_offset(mcu, options):
    """
    Called when multiple or unknown bootloader offsets exist for a family.
    'options' is a dict of {"Label (e.g. 28KiB bootloader)": "0x7000"}
    """
    choices = list(options.keys()) + ["No bootloader (0x0)", "Enter manually"]
    ans = questionary.select(
        f"Select bootloader offset for {mcu.upper()}:",
        choices=choices,
        style=custom_style
    ).ask()
    
    if ans == "Enter manually":
        return questionary.text("Enter HEX offset (e.g. 0x8000):", style=custom_style).ask()
    elif ans == "No bootloader (0x0)":
        return "0x0"
        
    return options[ans]
    
def prompt_mcu_family(mcu=None):
    """
    Called if totally unknown MCU name is provided.
    """
    choices = [
        "stm32",
        "lpc176x",
        "rp2040",
        "avr",
        "linux",
        "Enter manually"
    ]
    ans = questionary.select(
        f"Select MCU architecture family{' for ' + str(mcu) if mcu else ''}:",
        choices=choices,
        style=custom_style
    ).ask()
    
    if ans == "Enter manually":
         ans = questionary.text("Enter Klipper ARCH (e.g. stm32):", style=custom_style).ask()
    return ans
