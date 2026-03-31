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
        cfg_path = os.path.expanduser('~/kace/printer.cfg')
        sftp.put(cfg_path, dest)
        
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"\033[91mDeployment failed: {e}\033[0m")

def deploy_usb(user_data):
    """Deploys the generated printer.cfg (and firmware if exists) to a USB/SD card."""
    try:
        import questionary
        from core.style import custom_style
        
        dest = questionary.text(
            "Enter USB/SD Card mount path (e.g. D:\\ or /media/usb):",
            style=custom_style
        ).ask()
        
        if not dest or not os.path.isdir(dest):
            print(f"\033[91mDeployment failed: Invalid path or directory does not exist: {dest}\033[0m")
            return
            
        print(f"Copying printer.cfg to {dest}...")
        cfg_path = os.path.expanduser('~/kace/printer.cfg')
        shutil.copy2(cfg_path, os.path.join(dest, 'printer.cfg'))
        
        # Optionally copy firmware if exists
        for ext in ['klipper.bin', 'klipper.uf2', 'klipper.elf.hex']:
            firmware_bin = os.path.expanduser(f'~/kace/{ext}')
            if os.path.exists(firmware_bin):
                print(f"Found compiled firmware! Copying {ext} to {dest}...")
                shutil.copy2(firmware_bin, os.path.join(dest, ext))
            
        print("\033[92mUSB Deployment Successful!\033[0m")
    except Exception as e:
        print(f"\033[91mDeployment failed: {e}\033[0m")

def deploy_local(user_data):
    """Copies the generated printer.cfg to a local folder on the PC."""
    try:
        import questionary
        from core.style import custom_style
        
        dest = questionary.text(
            "Enter local destination folder path (e.g. C:\\3DPrinter or ~/Documents):",
            style=custom_style
        ).ask()
        
        if not dest:
            return

        dest = os.path.expanduser(dest)
        
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
            
        print(f"Copying printer.cfg to {dest}...")
        cfg_path = os.path.expanduser('~/kace/printer.cfg')
        shutil.copy2(cfg_path, os.path.join(dest, 'printer.cfg'))
        
        # Optionally copy firmware to local folder too
        for ext in ['klipper.bin', 'klipper.uf2', 'klipper.elf.hex']:
            firmware_bin = os.path.expanduser(f'~/kace/{ext}')
            if os.path.exists(firmware_bin):
                print(f"Found compiled firmware! Copying {ext} to {dest}...")
                shutil.copy2(firmware_bin, os.path.join(dest, ext))
                
        print(f"\033[92mSuccessfully saved to {dest}!\033[0m")
    except Exception as e:
        print(f"\033[91mSave failed: {e}\033[0m")
