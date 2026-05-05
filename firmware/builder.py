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
        
    # --- Summary & Confirmation Segment ---
    import questionary
    from core.style import custom_style

    def format_flash(f):
        mapping = {
            "0x0": "No bootloader",
            "0x2000": "8KiB bootloader",
            "0x4000": "16KiB bootloader",
            "0x7000": "28KiB bootloader",
            "0x8000": "32KiB bootloader",
            "0x10000": "64KiB bootloader",
            "0x20000": "128KiB bootloader"
        }
        return f"{mapping[f]} ({f})" if f in mapping else f

    while True:
        arch = config_dict.get("CONFIG_MCU", "Unknown").replace('"', '')
        model = derived_mcu if derived_mcu else "Unknown"
        flash = config_dict.get("CONFIG_FLASH_START", "0x0")
        comm = "USB" if config_dict.get("CONFIG_USB") == "y" else \
               "CAN" if config_dict.get("CONFIG_CANBUS") == "y" else \
               "UART" if config_dict.get("CONFIG_SERIAL") == "y" else \
               "SPI" if config_dict.get("CONFIG_SPI") == "y" else "Unknown"
               
        print("\n\033[96m=================================================\033[0m")
        print("\033[1m Klipper Firmware Target Summary\033[0m")
        print("\033[96m=================================================\033[0m")
        print(f" Architecture            : \033[93m{arch.upper()}\033[0m")
        print(f" Processor Model         : \033[93m{model.upper()}\033[0m")
        print(f" Bootloader Offset       : \033[93m{format_flash(flash)}\033[0m")
        print(f" Communication Interface : \033[93m{comm}\033[0m")
        
        clock = config_dict.get("CONFIG_CLOCK_FREQ")
        if clock:
            print(f" Clock Frequency         : \033[93m{int(clock)//1000000} MHz\033[0m")
            
        print(f" USB IDs / Serial Path   : \033[93m{mcu_path if mcu_path else 'Not Detected'}\033[0m")
        print("\033[96m=================================================\033[0m\n")
        
        choices = [
            "✅ Compile Firmware Now",
            "✏️ Edit Architecture",
            "✏️ Edit Processor Model",
            "✏️ Edit Bootloader Offset",
            "✏️ Edit Communication Interface"
        ]
        if clock:
            choices.append("✏️ Edit Clock Frequency")
        choices.append("❌ Abort")

        ans = questionary.select("Is this configuration correct?", choices=choices, style=custom_style).ask()
        
        if ans == "✅ Compile Firmware Now":
            break
        elif ans == "❌ Abort" or ans is None:
            return {"status": "error", "message": "Compilation aborted by user."}
        elif ans == "✏️ Edit Architecture":
            new_arch = questionary.text("Enter Kconfig Architecture (e.g. stm32, lpc176x):", default=arch, style=custom_style).ask()
            if new_arch: config_dict["CONFIG_MCU"] = f'"{new_arch}"'
        elif ans == "✏️ Edit Processor Model":
            new_model = questionary.text("Enter Processor Model (e.g. stm32f446):", default=model, style=custom_style).ask()
            if new_model: derived_mcu = new_model
        elif ans == "✏️ Edit Bootloader Offset":
            opts = [
                "No bootloader (0x0)", "8KiB bootloader (0x2000)", "16KiB bootloader (0x4000)",
                "28KiB bootloader (0x7000)", "32KiB bootloader (0x8000)", "64KiB bootloader (0x10000)",
                "128KiB bootloader (0x20000)", "Enter manually"
            ]
            f_ans = questionary.select("Select Bootloader Offset:", choices=opts, style=custom_style).ask()
            if f_ans == "Enter manually":
                f_ans = questionary.text("Enter HEX offset (e.g. 0x8000):", default=flash, style=custom_style).ask()
                if f_ans: config_dict["CONFIG_FLASH_START"] = f_ans
            elif f_ans:
                config_dict["CONFIG_FLASH_START"] = f_ans.split(" (")[1].replace(")", "")
        elif ans == "✏️ Edit Communication Interface":
            c_ans = questionary.select("Select Interface:", choices=["USB", "UART", "CAN", "SPI"], style=custom_style).ask()
            if c_ans:
                config_dict["CONFIG_USB"] = "y" if c_ans == "USB" else "n"
                config_dict["CONFIG_SERIAL"] = "y" if c_ans == "UART" else "n"
                config_dict["CONFIG_CANBUS"] = "y" if c_ans == "CAN" else "n"
                config_dict["CONFIG_SPI"] = "y" if c_ans == "SPI" else "n"
        elif ans == "✏️ Edit Clock Frequency":
            clk = questionary.text("Enter Clock Frequency in Hz (e.g. 120000000):", default=clock, style=custom_style).ask()
            if clk: config_dict["CONFIG_CLOCK_FREQ"] = clk
    # --------------------------------------
        
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

        subprocess.run(
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
