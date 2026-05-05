import glob
import re
import os
import questionary
from core.style import custom_style

def discover_mcu_hardware(interactive=True):
    """
    Auto-discovers the MCU via various paths or active Klipper configs.
    Returns a dictionary of:
    - mcu_path (e.g. /dev/ttyUSB0)
    - derived_mcu (e.g. stm32f103)
    - hint (e.g. usb, uart, can)
    """
    ports = glob.glob('/dev/serial/by-id/*')
    
    # Debian Bookworm udev bug fallback
    if not ports:
        ports = glob.glob('/dev/serial/by-path/*')
        
    # GPIO UART fallbacks
    for p in ['/dev/ttyAMA0', '/dev/ttyS0']:
        if os.path.exists(p) and p not in ports:
            ports.append(p)
            
    # Active Klipper Config Fallback (if they already have Mainsail running)
    cfg_path = os.path.expanduser("~/printer_data/config/printer.cfg")
    if not ports and os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r") as f:
                content = f.read()
                # Find [mcu] section and extract serial:
                mcu_match = re.search(r'\[mcu\][^\[]*serial:\s*([^\s\n]+)', content, re.MULTILINE)
                if mcu_match:
                    found_port = mcu_match.group(1).strip()
                    if found_port not in ports:
                        ports.append(found_port)
        except Exception:
            pass

    context = {"mcu_path": None, "derived_mcu": None, "hint": None}
    
    if not ports:
        if not interactive:
            return context
        ans = questionary.text("No serial devices found. Enter MCU path manually (or skip):", style=custom_style).ask()
        if ans:
             context["mcu_path"] = ans
             context["hint"] = "manual"
        return context
    
    if interactive:
        choices = ports + ["Enter manually...", "Skip detection"]
        choice = questionary.select("Select connected MCU:", choices=choices, style=custom_style).ask()
        
        if choice == "Skip detection" or choice is None:
            context["hint"] = "skip"
            return context
            
        if choice == "Enter manually...":
            context["mcu_path"] = questionary.text("Enter MCU path manually:", style=custom_style).ask()
            context["hint"] = "manual"
            return context
    else:
        klipper_ports = [p for p in ports if "Klipper" in p]
        choice = klipper_ports[0] if klipper_ports else ports[0]
        
    context["mcu_path"] = choice
    
    # Extract MCU name and interface Hint
    # Example format: usb-Klipper_stm32f103_123456-if00 or usb-Klipper_lpc1768-if00
    match = re.search(r'(usb|can|uart|tty)[_-]Klipper_([a-zA-Z0-9]+)', choice)
    if match:
        context["hint"] = match.group(1).lower()
        if context["hint"] == "tty":
            context["hint"] = "uart"
        context["derived_mcu"] = match.group(2).lower()
    else:
        # Fallback regex for standard usb paths without specific comm prefix
        match_simple = re.search(r'usb-Klipper_([a-zA-Z0-9]+)', choice)
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
