import os
import sys
from core.scraper import fetch_config_list, fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.generator import generate_config
from core.deployer import deploy_config

def print_header():
    print("\033[94m" + "="*60 + "\033[0m")
    print("\033[92m" + "   _  __  ___   _____  ______" + "\033[0m")
    print("\033[92m" + "  / |/ / / _ | / ___/ / __  /" + "\033[0m")
    print("\033[92m" + " /    / / __ |/ /__  / /___/ " + "\033[0m")
    print("\033[92m" + "/_/|_/ /_/ |_|\___/ /_____/  " + "\033[0m")
    print("\033[94m" + "  Klipper Automated Configuration Ecosystem" + "\033[0m")
    print("\033[94m" + "="*60 + "\033[0m")

def main():
    print_header()
    
    # Milestone 3 & 4: Interactive Wizard
    user_data = run_wizard()
    
    # Milestone 1: The Scraper
    print(f"\n\033[96m[1/3]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m...")
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg)
    
    # Milestone 2: The Template Generator
    print("\033[96m[2/3]\033[0m Generating printer.cfg...")
    generate_config(parsed_data, user_data)
    
    # SSH Deployment
    if user_data.get('deploy_ssh'):
        print("\033[96m[3/3]\033[0m Deploying to Klipper host via SSH...")
        deploy_config(user_data)
    else:
        print("\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully!")

if __name__ == "__main__":
    main()
