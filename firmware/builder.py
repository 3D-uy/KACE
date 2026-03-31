import os
import shutil
import subprocess
from .derivation import derive_config
from .generator import generate_firmware_config
from .validator import validate_config

def build_firmware_orchestrator(mcu_path=None, derived_mcu=None, hint=None, klipper_path="~/klipper", output_dir="~/kace"):
    """
    Orchestrates the firmware derivation, generation, validation, and build process.
    Returns a structured dictionary with results.
    """
    klipper_path = os.path.expanduser(klipper_path)
    output_dir = os.path.expanduser(output_dir)

    # 1. Derive Configuration
    try:
        config_dict = derive_config(derived_mcu, hint)
    except Exception as e:
        return {"status": "error", "message": f"Configuration derivation failed: {str(e)}"}
        
    # 2. Generate minimal .config
    success, msg = generate_firmware_config(config_dict, klipper_path)
    if not success:
         return {"status": "error", "message": msg}

    try:
        # 3. Resolve full configuration with olddefconfig
        subprocess.run(
            ["make", "olddefconfig"],
            cwd=klipper_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # 4. Post-olddefconfig Validation
        val_success, val_msg = validate_config(klipper_path)
        if not val_success:
             return {"status": "error", "message": val_msg}
        
        # 5. Clean and Compile
        subprocess.run(
            ["make", "clean"],
            cwd=klipper_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        build_cmd = ["make"]
        try:
            nproc = subprocess.check_output(["nproc"]).decode().strip()
            build_cmd.append(f"-j{nproc}")
        except Exception:
            pass # Fallback if nproc is not available

        res = subprocess.run(
            build_cmd,
            cwd=klipper_path,
            check=True,
            capture_output=True,
            text=True
        )
            
        # 6. Locate output artifact and copy
        out_path = os.path.join(klipper_path, "out")
        expected_outputs = ["klipper.bin", "klipper.uf2", "klipper.elf.hex"]
        
        os.makedirs(output_dir, exist_ok=True)
            
        for binary in expected_outputs:
            p = os.path.join(out_path, binary)
            if os.path.exists(p):
                dest = os.path.join(output_dir, binary)
                shutil.copy2(p, dest)
                return {
                    "status": "success",
                    "mcu": derived_mcu,
                    "firmware": binary,
                    "path": dest
                }
                
        return {"status": "error", "message": "Firmware compiled, but no recognized output file (klipper.bin/.uf2/.elf.hex) found."}
        
    except subprocess.CalledProcessError as e:
         return {"status": "error", "message": f"Failed to compile firmware (Make error {e.returncode}):\n{e.stderr}"}
    except FileNotFoundError:
         return {"status": "error", "message": "Failed to compile firmware: 'make' command not found. build-essential package required."}
    except Exception as e:
         return {"status": "error", "message": f"An unexpected error occurred during build: {str(e)}"}
