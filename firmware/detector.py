import glob
import re
import questionary
from core.style import custom_style

def discover_mcu_hardware():
    """
    Auto-discovers the MCU via /dev/serial/by-id/.
    Returns a dictionary of:
    - mcu_path (e.g. /dev/ttyUSB0)
    - derived_mcu (e.g. stm32f103)
    - hint (e.g. usb, uart, can)
    """
    ports = glob.glob('/dev/serial/by-id/*')
    context = {"mcu_path": None, "derived_mcu": None, "hint": None}
    
    if not ports:
        ans = questionary.text("No serial devices found. Enter MCU path manually (or skip):", style=custom_style).ask()
        if ans:
             context["mcu_path"] = ans
             context["hint"] = "manual"
        return context
    
    choices = ports + ["Enter manually...", "Skip detection"]
    choice = questionary.select("Select connected MCU:", choices=choices, style=custom_style).ask()
    
    if choice == "Skip detection" or choice is None:
        context["hint"] = "skip"
        return context
        
    if choice == "Enter manually...":
        context["mcu_path"] = questionary.text("Enter MCU path manually:", style=custom_style).ask()
        context["hint"] = "manual"
        return context
        
    context["mcu_path"] = choice
    
    # Extract MCU name and interface Hint
    # Example format: usb-Klipper_stm32f103_123456-if00
    match = re.search(r'(usb|can|uart|tty)[_-]Klipper_([a-zA-Z0-9]+)_', choice)
    if match:
        context["hint"] = match.group(1).lower()
        if context["hint"] == "tty":
            context["hint"] = "uart"
        context["derived_mcu"] = match.group(2).lower()
    else:
        # Fallback regex for standard usb paths without specific comm prefix
        match_simple = re.search(r'usb-Klipper_([a-zA-Z0-9]+)_', choice)
        if match_simple:
            context["hint"] = "usb"
            context["derived_mcu"] = match_simple.group(1).lower()
        else:
            # Look for loose hints
            if "usb" in choice.lower():
                context["hint"] = "usb"
            elif "tty" in choice.lower() or "uart" in choice.lower():
                context["hint"] = "uart"
            elif "can" in choice.lower():
                context["hint"] = "can"
            
    return context
