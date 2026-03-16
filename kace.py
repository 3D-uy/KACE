import os
import sys
import time
from core.scraper import fetch_config_list, fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.generator import generate_config

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
    
    print(f"\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully at \033[93m{os.path.abspath('printer.cfg')}\033[0m")

    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
