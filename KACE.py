import os
import sys
from core.scraper import fetch_config_list, fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.generator import generate_config
from core.deployer import deploy_config

def print_header():
    print("\033[94m" + "="*60 + "\033[0m")
    print("\033[96m" + "    __ __  ___   ______  ______" + "\033[0m")
    print("\033[96m" + "   / //_/ /   | / ____/ / ____/" + "\033[0m")
    print("\033[92m" + "  / ,<   / /| |/ /     / __/   " + "\033[0m")
    print("\033[92m" + " / /| | / ___ / /___  / /___   " + "\033[0m")
    print("\033[93m" + "/_/ |_|/_/  |_\____/ /_____/   " + "\033[0m")
    print("\033[97m\033[1m" + "  Klipper Automated Configuration Ecosystem" + "\033[0m")
    print("\033[94m" + "="*60 + "\033[0m")

def main():
    print_header()
    
    # Milestone 3 & 4: Interactive Wizard
    user_data = run_wizard()
    
    # Milestone 1: The Scraper
    print(f"\n\033[91m[1/3]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m...", end="", flush=True)
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg, user_data['board'])
    print(f"\r\033[92m[1/3]\033[0m Fetching configuration for \033[93m{user_data['board']}\033[0m... Done!")
    
    # Milestone 2: The Template Generator
    print("\033[91m[2/3]\033[0m Generating printer.cfg...", end="", flush=True)
    generate_config(parsed_data, user_data)
    print("\r\033[92m[2/3]\033[0m Generating printer.cfg... Done!")
    
    # SSH Deployment
    if user_data.get('deploy_choice') == "Deploy to Klipper host via SSH":
        print("\033[91m[3/3]\033[0m Deploying to Klipper host via SSH...")
        deploy_config(user_data)
        print("\033[92m[3/3]\033[0m Deploying to Klipper host via SSH... Done!")
    elif user_data.get('deploy_choice') == "Start a temporary web server to download to PC":
        print("\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully!")
        print("\033[96m[3/3]\033[0m Starting temporary web server...")
        import http.server
        import socketserver
        PORT = 8080
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\033[93mDownload your file at: http://<raspberry-pi-ip>:{PORT}/printer.cfg\033[0m")
            print("Press Ctrl+C to stop the server and exit.")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
    else:
        print(f"\n\033[92mSUCCESS:\033[0m printer.cfg generated successfully at \033[93m{os.path.abspath('printer.cfg')}\033[0m")

if __name__ == "__main__":
    main()
