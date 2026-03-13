import os
import sys
from core.scraper import fetch_config_list, fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.generator import generate_config
from core.deployer import deploy_config

def main():
    print("=======================================================")
    print(" Welcome to KACE (Klipper Automated Configuration Ecosystem) ")
    print("=======================================================")
    
    # Milestone 3 & 4: Interactive Wizard
    user_data = run_wizard()
    
    # Milestone 1: The Scraper
    print(f"\nFetching configuration for {user_data['board']}...")
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg)
    
    # Milestone 2: The Template Generator
    print("\nGenerating printer.cfg...")
    generate_config(parsed_data, user_data)
    
    # SSH Deployment
    if user_data.get('deploy_ssh'):
        print("\nDeploying to Klipper host via SSH...")
        deploy_config(user_data)
    else:
        print("\nDone! printer.cfg has been generated successfully in the current directory.")

if __name__ == "__main__":
    main()
