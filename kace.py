import os
import sys
import time
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
    print("")

def main():
    print_header()
    
    # Milestone 3 & 4: Interactive Wizard
    user_data = run_wizard()
    
    # Milestone 1: The Scraper
    print(f"\n\033[91m[1/3]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m...", end="", flush=True)
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg, user_data['board'])
    time.sleep(0.5)
    print(f"\r\033[92m[1/3]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m... Done!")
    
    # Milestone 2: The Template Generator
    print("\033[91m[2/3]\033[0m Generating printer.cfg...", end="", flush=True)
    generate_config(parsed_data, user_data)
    time.sleep(0.5)
    print("\r\033[92m[2/3]\033[0m Generating printer.cfg... Done!")
    
    cfg_path = os.path.expanduser('~/kace/printer.cfg')
    print(f"\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully at \033[93m{cfg_path}\033[0m")

    # Milestone 3: Firmware Compilation
    mcu = user_data.get('mcu_type')
    hint = user_data.get('mcu_hint')
    if mcu or hint == "manual":
        # If MCU was skipped completely or the user hit enter manually, ask what the target is
        prompt_mcu = mcu if mcu else "manually selected board"
        ans = questionary.confirm(f"Do you want to automatically compile Klipper firmware for your {prompt_mcu}?").ask()
        if ans:
            from firmware.builder import build_firmware_orchestrator
            print("\n\033[91m[3/3]\033[0m Rebuilding Klipper firmware for your controller...", flush=True)
            result = build_firmware_orchestrator(
                mcu_path=user_data.get('mcu_path'),
                derived_mcu=mcu,
                hint=hint,
                output_dir="~/kace"
            )
            
            if result.get("status") == "success":
                print(f"\033[92mSUCCESS:\033[0m Firmware built locally at {result.get('path')}")
                # Save actual MCU used to user_data for deployment references
                user_data['mcu_type'] = result.get('mcu')
            else:
                print(f"\n\033[91mERROR:\033[0m {result.get('message')}")
    else:
        print("\n\033[93mSkipping firmware compilation (no MCU designated).\033[0m")

    # Milestone 5: Deployment
    deploy_method = questionary.select(
        "\nSelect Deployment Method:",
        choices=["None (Done)", "Local Folder (PC)", "USB / SD Card", "SSH (Push to host)"],
        style=custom_style
    ).ask()

    if deploy_method == "USB / SD Card":
        deploy_usb(user_data)
    elif deploy_method == "Local Folder (PC)":
        deploy_local(user_data)
    elif deploy_method == "SSH (Push to host)":
        user_data['host'] = questionary.text("Enter SSH Host (e.g. 192.168.1.100):", style=custom_style).ask()
        user_data['user'] = questionary.text("Enter SSH User (e.g. pi):", default="pi", style=custom_style).ask()
        user_data['password'] = questionary.password("Enter SSH Password:", style=custom_style).ask()
        user_data['dest_path'] = questionary.text("Enter Destination Path:", default="~/printer_data/config/", style=custom_style).ask()
        if user_data['host'] and user_data['user'] and user_data['dest_path']:
            deploy_config(user_data)

    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
