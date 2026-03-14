import os
import sys
import time
import shutil
import subprocess
import questionary
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

def deploy_local(config_path):
    """Deploys the generated config to the local Klipper directory."""
    target = os.path.join(config_path, "printer.cfg")
    backup = os.path.join(config_path, f"printer.cfg.kace.{int(time.time())}.bak")
    
    try:
        if os.path.exists(target):
            shutil.copy2(target, backup)
            print(f"\033[94m>>> Backup created: {backup}\033[0m")
        
        shutil.copy2("printer.cfg", target)
        print(f"\033[92m>>> Configuration deployed to {target}\033[0m")
        
        if questionary.confirm("Would you like to restart Klipper now?", default=True).ask():
            print("\033[96m>>> Restarting Klipper...\033[0m")
            subprocess.run(["sudo", "systemctl", "restart", "klipper"], check=False)
            print("\033[92m>>> Klipper restart command sent!\033[0m")
        else:
            print("\033[93m>>> Manual restart required in your web interface.\033[0m")
    except Exception as e:
        print(f"\033[91mERROR during local deployment: {e}\033[0m")

def deploy_ssh(deploy_data):
    """Deploys via SSH."""
    try:
        import paramiko
        print(f"\033[96m>>> Connecting to {deploy_data['host']}...\033[0m")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # We don't ask for password here for security, assume SSH keys or prompt
        try:
            ssh.connect(deploy_data['host'], username=deploy_data['user'], timeout=10)
        except paramiko.AuthenticationException:
            password = questionary.password(f"Enter SSH password for {deploy_data['user']}:").ask()
            ssh.connect(deploy_data['host'], username=deploy_data['user'], password=password)

        sftp = ssh.open_sftp()
        remote_path = os.path.join(deploy_data['config_path'], "printer.cfg")
        
        print("\033[96m>>> Uploading printer.cfg...\033[0m")
        sftp.put("printer.cfg", remote_path)
        sftp.close()
        
        if questionary.confirm("Would you like to restart Klipper now?", default=True).ask():
            print("\033[96m>>> Restarting Klipper...\033[0m")
            ssh.exec_command("sudo systemctl restart klipper")
            print("\033[92m>>> Klipper restart command sent!\033[0m")
        else:
            print("\033[93m>>> Manual restart required in your web interface.\033[0m")
            
        ssh.close()
        print("\033[92m>>> Deployment successful!\033[0m")
    except ImportError:
        print("\033[91mERROR: 'paramiko' library not found. Install it with: pip install paramiko\033[0m")
    except Exception as e:
        print(f"\033[91mERROR during SSH deployment: {e}\033[0m")

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

    # Deployment Phase
    deploy = user_data.get("deploy", {})
    if deploy.get("method") == "Local (This Pi)":
        print("\n\033[91m[3/3]\033[0m Deploying locally...")
        deploy_local(deploy["config_path"])
    elif deploy.get("method") == "SSH (Remote Pi)":
        print("\n\033[91m[3/3]\033[0m Deploying via SSH...")
        deploy_ssh(deploy)
    else:
        print("\n\033[93m[3/3]\033[0m Generation complete. Manual upload required.")

    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
