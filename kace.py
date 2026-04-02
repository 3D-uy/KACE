#!/usr/bin/env python3

__version__ = "v0.1.0-beta"

import os
import sys
import time

# ── Early argument handling (no heavy imports needed) ─────────
if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-v"):
    print(f"KACE {__version__}")
    sys.exit(0)

import questionary
from core.scraper import fetch_config_list, fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.style import custom_style
from core.generator import generate_config
from core.deployer import deploy_config, deploy_usb, deploy_local, deploy_avrdude

def print_header():
    # Clear screen KIAUH-style
    os.system('clear' if os.name == 'posix' else 'cls')

    # ANSI Escape Codes
    G = "\033[92m"  # Green
    Y = "\033[93m"  # Yellow
    C = "\033[96m"  # Cyan
    B = "\033[1m"   # Bold
    R = "\033[0m"   # Reset

    raw_logo = [
        "██╗  ██╗ █████╗  ██████╗███████╗",
        "██║ ██╔╝██╔══██╗██╔════╝██╔════╝",
        "█████╔╝ ███████║██║     █████╗  ",
        "██╔═██╗ ██╔══██║██║     ██╔══╝  ",
        "██║  ██╗██║  ██║╚██████╗███████╗",
        "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝"
    ]

    print("")
    max_len = max(len(l) for l in raw_logo)
    c1 = (46, 204, 113) # Vibrant Green
    c2 = (52, 152, 219) # Vibrant Blue
    
    for line in raw_logo:
        colored_line = ""
        for i, char in enumerate(line):
            ratio = i / max(1, max_len - 1)
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        print(f"  {colored_line}\033[0m")
    
    print(f"  {C}──────────────────────────────────────────{R}")
    print(f"  {B}{C}Klipper Automated Configuration Ecosystem{R}")
    print(f"  {Y}                          {__version__}{R}")
    print("")

def print_summary(user_data: dict):
    """Print final summary with output paths and next steps."""
    G = "\033[92m"
    Y = "\033[93m"
    C = "\033[96m"
    B = "\033[1m"
    R = "\033[0m"

    fw_path = user_data.get('firmware_path', '~/kace/klipper.bin')
    cfg_path = os.path.expanduser('~/kace/printer.cfg')

    print("")
    print(f"  {G}══════════════════════════════════════════{R}")
    print(f"  {B}{G}  ✅ Setup Complete{R}")
    print(f"  {G}══════════════════════════════════════════{R}")
    print("")
    print(f"  {B}Firmware:{R} {Y}{fw_path}{R}")
    print(f"  {B}Config:  {R} {Y}{cfg_path}{R}")
    print("")
    print(f"  {B}{C}Next steps:{R}")
    print(f"  {C}1.{R} Flash firmware to your board")
    print(f"  {C}2.{R} Upload printer.cfg to Klipper")
    print(f"  {C}3.{R} Restart Klipper")
    print("")
    print(f"  {G}──────────────────────────────────────────{R}")
    print("")


def main():
    print_header()
    
    # Milestone 3 & 4: Interactive Wizard
    try:
        user_data = run_wizard()
    except (KeyboardInterrupt, EOFError):
        print("\n\033[93mSetup cancelled by user.\033[0m")
        sys.exit(0)
    except ImportError as e:
        print(f"\n\033[91mERROR:\033[0m Missing dependency: {e}")
        print("\033[93mRun: pip3 install -r requirements.txt --break-system-packages\033[0m")
        sys.exit(1)

    # ==========================================
    # PHASE 1: FIRMWARE COMPILATION & DEPLOYMENT
    # ==========================================
    mcu = user_data.get('mcu_type')
    hint = user_data.get('mcu_hint')
    if mcu or hint == "manual":
        # If MCU was skipped completely or the user hit enter manually, ask what the target is
        prompt_mcu = mcu if mcu else "manually selected board"
        ans = questionary.confirm(f"Do you want to automatically compile Klipper firmware for your {prompt_mcu}?").ask()
        if ans:
            from firmware.builder import build_firmware_orchestrator
            print("\n\033[91m[*]\033[0m Rebuilding Klipper firmware for your controller...", flush=True)
            result = build_firmware_orchestrator(
                mcu_path=user_data.get('mcu_path'),
                derived_mcu=mcu,
                hint=hint,
                output_dir="~/kace"
            )
            
            if result.get("status") == "success":
                print(f"\033[92mSUCCESS:\033[0m Firmware built locally at {result.get('path')}")
                user_data['mcu_type'] = result.get('mcu') # Save actual MCU used to user_data
                
                # --- Firmware Deployment ---
                deploy_options = ["None (Done)", "Local Folder (PC)", "USB / SD Card"]
                if result.get('firmware') == 'klipper.elf.hex':
                    deploy_options.insert(1, "Flash via USB (avrdude)")

                deploy_fw = questionary.select(
                    "\nSelect Deployment Method for Firmware (klipper.bin/.uf2/.hex):",
                    choices=deploy_options,
                    style=custom_style
                ).ask()
                
                if deploy_fw == "USB / SD Card":
                    deploy_usb(user_data, artifact_type="firmware")
                elif deploy_fw == "Local Folder (PC)":
                    deploy_local(user_data, artifact_type="firmware")
                elif deploy_fw == "Flash via USB (avrdude)":
                    deploy_avrdude(user_data, result.get("path"), result.get("mcu"))

            else:
                print(f"\n\033[91mERROR:\033[0m {result.get('message')}")
    else:
        print("\n\033[93mSkipping firmware compilation (no MCU designated).\033[0m")
        
    # ==========================================
    # PHASE 2: CONFIGURATION FETCH & GENERATION
    # ==========================================
    print(f"\n\033[91m[*]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m...", end="", flush=True)
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg, user_data['board'])
    time.sleep(0.5)
    print(f"\r\033[92m[*]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m... Done!")
    
    # --- Multi-Z Pin Verification (Before Generation) ---
    z_motors = int(user_data.get('z_motors', 1))
    if z_motors > 1:
        available_driver_keys = sorted([k for k in parsed_data.keys() if k.startswith("extruder") and k != "extruder"])
        for i in range(2, z_motors + 1):
            motor_name = f"stepper_z{i - 1}"
            
            if motor_name in parsed_data:
                continue

            print(f"\n\033[96m>>> Mapping pins for [ {motor_name} ] ...\033[0m")
            if not available_driver_keys:
                print("\033[93mWarning: Your board does not have enough available stepper drivers in its config for this Z motor.\033[0m")
            
            driver_choices = []
            for dk in available_driver_keys:
                label = dk.replace("extruder", "E")
                if dk == "extruder1":
                    label = "E1 (recommended)"
                driver_choices.append({"name": label, "value": dk})
                
            driver_choices.append({"name": "Custom pin assignment", "value": "custom"})
            driver_choices.append({"name": "Quit setup", "value": "quit"})
            
            selected_driver = questionary.select(
                f"Select driver for {motor_name.upper()}:",
                choices=driver_choices,
                style=custom_style
            ).ask()
            
            if selected_driver == "quit" or selected_driver is None:
                print("\n\033[91mSetup aborted. Missing pins for Z motors.\033[0m")
                sys.exit(1)
                
            if selected_driver == "custom":
                print(f"\nAssigning custom pins for {motor_name}:")
                step_pin = questionary.text(f"Enter step_pin (e.g. PC4):", style=custom_style).ask()
                dir_pin = questionary.text(f"Enter dir_pin (e.g. PA6):", style=custom_style).ask()
                en_pin = questionary.text(f"Enter enable_pin (e.g. !PC5):", style=custom_style).ask()
                
                if not step_pin or not dir_pin or not en_pin:
                    print("\n\033[91mError: Valid pins are required to proceed. Aborting.\033[0m")
                    sys.exit(1)
                    
                parsed_data[motor_name] = {
                    "step_pin": step_pin,
                    "dir_pin": dir_pin,
                    "enable_pin": en_pin
                }
                
                driver_type = user_data.get("driver_type", "None (Standard)")
                driver_mode = user_data.get("driver_mode", "")
                if "TMC" in driver_type and driver_mode in ["UART", "SPI"]:
                    uart_pin = questionary.text(f"Enter {driver_mode.lower()}_pin for {motor_name}:", style=custom_style).ask()
                    if not uart_pin:
                        print(f"\n\033[91mError: {driver_mode} pin is critically required. Aborting.\033[0m")
                        sys.exit(1)
                    tmc_section = f"{driver_type.lower()} {motor_name}"
                    pin_key = "uart_pin" if driver_mode == "UART" else "cs_pin"
                    parsed_data[tmc_section] = {pin_key: uart_pin, "run_current": "0.650"}
            else:
                src_data = parsed_data[selected_driver]
                parsed_data[motor_name] = {
                    "step_pin": src_data.get("step_pin", ""),
                    "dir_pin": src_data.get("dir_pin", ""),
                    "enable_pin": src_data.get("enable_pin", "")
                }
                
                driver_type = user_data.get("driver_type", "None (Standard)")
                driver_mode = user_data.get("driver_mode", "")
                if "TMC" in driver_type:
                    dest_tmc = f"{driver_type.lower()} {motor_name}"
                    found_tmc = False
                    for possible_tmc in ["tmc2209", "tmc2208", "tmc2130", "tmc5160", "tmc2225", "tmc2240"]:
                        src_tmc = f"{possible_tmc} {selected_driver}"
                        if src_tmc in parsed_data:
                            parsed_data[dest_tmc] = parsed_data[src_tmc].copy()
                            del parsed_data[src_tmc]
                            found_tmc = True
                            break
                    if not found_tmc and driver_mode in ["UART", "SPI"]:
                        print(f"\n\033[91mError: No {driver_mode} pin mapping found on this board for {selected_driver}.\033[0m")
                        print("\033[93mGeneration aborted to prevent missing parameters.\033[0m")
                        sys.exit(1)
                
                del parsed_data[selected_driver]
                available_driver_keys.remove(selected_driver)

    print("\033[91m[*]\033[0m Generating printer.cfg...", end="", flush=True)
    generate_config(parsed_data, user_data)
    time.sleep(0.5)
    print("\r\033[92m[*]\033[0m Generating printer.cfg... Done!")
    
    cfg_path = os.path.expanduser('~/kace/printer.cfg')
    print(f"\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully at \033[93m{cfg_path}\033[0m")

    # ==========================================
    # PHASE 3: CONFIGURATION DEPLOYMENT
    # ==========================================
    deploy_cfg = questionary.select(
        "\nSelect Deployment Method for Configuration (printer.cfg):",
        choices=["None (Done)", "Local Folder (PC)", "USB / SD Card", "SSH (Push to host)"],
        style=custom_style
    ).ask()

    if deploy_cfg == "USB / SD Card":
        deploy_usb(user_data, artifact_type="config")
    elif deploy_cfg == "Local Folder (PC)":
        deploy_local(user_data, artifact_type="config")
    elif deploy_cfg == "SSH (Push to host)":
        user_data['host'] = questionary.text("Enter SSH Host (e.g. 192.168.1.100):", style=custom_style).ask()
        user_data['user'] = questionary.text("Enter SSH User (e.g. pi):", default="pi", style=custom_style).ask()
        user_data['password'] = questionary.password("Enter SSH Password:", style=custom_style).ask()
        user_data['dest_path'] = questionary.text("Enter Destination Path:", default="~/printer_data/config/", style=custom_style).ask()
        if user_data['host'] and user_data['user'] and user_data['dest_path']:
            deploy_config(user_data)

    time.sleep(0.5)
    print_summary(user_data)
    sys.exit(0)

if __name__ == "__main__":
    main()
