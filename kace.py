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
from core.deployer import deploy_config, deploy_usb, deploy_local

def print_header():
    # ANSI Escape Codes
    G = "\033[92m"  # Green
    Y = "\033[93m"  # Yellow
    C = "\033[96m"  # Cyan
    B = "\033[1m"   # Bold
    R = "\033[0m"   # Reset

    logo = [
        f"{G}██{Y}╗{G}  ██{Y}╗{G} █████{Y}╗{G}  ██████{Y}╗{G}███████{Y}╗",
        f"{G}██{Y}║{G} ██{Y}╔╝{G}██{Y}╔══{G}██{Y}╗{G}██{Y}╔════╝{G}██{Y}╔════╝",
        f"{G}█████{Y}╔╝{G} ███████{Y}║{G}██{Y}║{G}     █████{Y}╗",
        f"{G}██{Y}╔═{G}██{Y}╗{G} ██{Y}╔══{G}██{Y}║{G}██{Y}║{G}     ██{Y}╔══╝",
        f"{G}██{Y}║{G}  ██{Y}╗{G}██{Y}║{G}  ██{Y}║{Y}╚{G}██████{Y}╗{G}███████{Y}╗",
        f"{Y}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝"
    ]

    print("")
    for line in logo:
        print(f"  {line}")
    
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
                deploy_fw = questionary.select(
                    "\nSelect Deployment Method for Firmware (klipper.bin/.uf2):",
                    choices=["None (Done)", "Local Folder (PC)", "USB / SD Card"],
                    style=custom_style
                ).ask()
                
                if deploy_fw == "USB / SD Card":
                    deploy_usb(user_data, artifact_type="firmware")
                elif deploy_fw == "Local Folder (PC)":
                    deploy_local(user_data, artifact_type="firmware")

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
