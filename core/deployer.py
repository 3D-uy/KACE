import paramiko
import os
import shutil

def deploy_config(user_data):
    """Deploys the generated printer.cfg to the Klipper host via SSH/SCP."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"Connecting to {user_data['host']}...")
        ssh.connect(
            user_data['host'], 
            username=user_data['user'], 
            password=user_data['password']
        )
        
        sftp = ssh.open_sftp()
        
        # Expand user path (e.g., ~) if necessary
        dest = user_data['dest_path']
        if dest.startswith('~/'):
            # Simple expansion for common Klipper setups
            dest = dest.replace('~/', f"/home/{user_data['user']}/")
            
        print(f"Uploading printer.cfg to {dest}...")
        sftp.put('printer.cfg', dest)
        
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"\033[91mDeployment failed: {e}\033[0m")

def deploy_usb(user_data):
    """Deploys the generated printer.cfg (and firmware if exists) to a USB/SD card."""
    try:
        import questionary
        from core.wizard import custom_style
        
        dest = questionary.text(
            "Enter USB/SD Card mount path (e.g. D:\\ or /media/usb):",
            style=custom_style
        ).ask()
        
        if not dest or not os.path.isdir(dest):
            print(f"\033[91mDeployment failed: Invalid path or directory does not exist: {dest}\033[0m")
            return
            
        print(f"Copying printer.cfg to {dest}...")
        shutil.copy2('printer.cfg', os.path.join(dest, 'printer.cfg'))
        
        # Optionally copy klipper.bin if exists
        klipper_bin = os.path.expanduser('~/klipper/out/klipper.bin')
        if os.path.exists(klipper_bin):
            print(f"Found compiled firmware! Copying klipper.bin to {dest}...")
            shutil.copy2(klipper_bin, os.path.join(dest, 'klipper.bin'))
            
        print("\033[92mUSB Deployment Successful!\033[0m")
    except Exception as e:
        print(f"\033[91mDeployment failed: {e}\033[0m")
