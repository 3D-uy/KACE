import paramiko
import os

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
        print("Deployment successful!")
    except Exception as e:
        print(f"Deployment failed: {e}")
