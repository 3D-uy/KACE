import os
import shutil
import subprocess
from .derivation import derive_config
from .generator import generate_firmware_config
from .validator import validate_config
from core.translations import t

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
        return {"status": "error", "message": t("builder.derivation_failed", error=str(e))}
        
    # --- Summary & Confirmation Segment ---
    import questionary
    from core.style import custom_style

    def format_flash(f):
        mapping = {
            "0x0": t("builder.boot_no"),
            "0x2000": t("builder.boot_8k"),
            "0x4000": t("builder.boot_16k"),
            "0x7000": t("builder.boot_28k"),
            "0x8000": t("builder.boot_32k"),
            "0x10000": t("builder.boot_64k"),
            "0x20000": t("builder.boot_128k")
        }
        return f"{mapping[f]} ({f})" if f in mapping else f

    # ANSI color helpers (local scope)
    _G  = "\033[92m"    # green
    _Y  = "\033[93m"    # yellow
    _C  = "\033[96m"    # cyan
    _M  = "\033[95m"    # magenta
    _R  = "\033[0m"     # reset
    _B  = "\033[1m"     # bold
    _RE = "\033[91m"    # red

    while True:
        arch  = config_dict.get("CONFIG_MCU", "Unknown").replace('"', '')
        model = derived_mcu if derived_mcu else "Unknown"
        flash = config_dict.get("CONFIG_FLASH_START", "0x0")
        comm  = "USB" if config_dict.get("CONFIG_USB") == "y" else \
               "CAN" if config_dict.get("CONFIG_CANBUS") == "y" else \
               "UART" if config_dict.get("CONFIG_SERIAL") == "y" else \
               "SPI" if config_dict.get("CONFIG_SPI") == "y" else "Unknown"

        _SEP = "═" * 47

        def _fw_row(label, value):
            pad = " " * max(0, 25 - len(label))
            return f"  {_B}{_C}{label}{_R}{pad}: {_Y}{value}{_R}"

        print(f"\n  {_C}{_SEP}{_R}")
        print(f"  {_B}{_M}  {t('builder.summary_title')}{_R}")
        print(f"  {_C}{_SEP}{_R}")
        print(_fw_row(t("builder.architecture"),           arch.upper()))
        print(_fw_row(t("builder.processor"),              model.upper()))
        print(_fw_row(t("builder.bootloader"),             format_flash(flash)))
        print(_fw_row(t("builder.comm_interface"),         comm))

        clock = config_dict.get("CONFIG_CLOCK_FREQ")
        if clock:
            print(_fw_row(t("builder.clock"), f"{int(clock)//1000000} MHz"))

        print(_fw_row(t("builder.usb_path"),    mcu_path if mcu_path else t("builder.not_detected")))
        print(f"  {_C}{_SEP}{_R}\n")

        choices = [
            t("builder.compile_now"),
            t("builder.edit_arch"),
            t("builder.edit_proc"),
            t("builder.edit_boot"),
            t("builder.edit_comm"),
        ]
        if clock:
            choices.append(t("builder.edit_clock"))
        choices.append(t("builder.abort"))

        ans = questionary.select(t("builder.config_correct"), choices=choices, style=custom_style).ask()

        if ans == t("builder.compile_now"):
            break
        elif ans == t("builder.abort") or ans is None:
            return {"status": "error", "message": t("builder.compilation_aborted")}
        elif ans == t("builder.edit_arch"):
            new_arch = questionary.text(t("builder.enter_arch"), default=arch, style=custom_style).ask()
            if new_arch: config_dict["CONFIG_MCU"] = f'"{new_arch}"'
        elif ans == t("builder.edit_proc"):
            new_model = questionary.text(t("builder.enter_proc"), default=model, style=custom_style).ask()
            if new_model: derived_mcu = new_model
        elif ans == t("builder.edit_boot"):
            opts = [
                f"{t('builder.boot_no')} (0x0)", f"{t('builder.boot_8k')} (0x2000)", f"{t('builder.boot_16k')} (0x4000)",
                f"{t('builder.boot_28k')} (0x7000)", f"{t('builder.boot_32k')} (0x8000)", f"{t('builder.boot_64k')} (0x10000)",
                f"{t('builder.boot_128k')} (0x20000)", t("builder.enter_manual")
            ]
            f_ans = questionary.select(t("builder.select_boot"), choices=opts, style=custom_style).ask()
            if f_ans == t("builder.enter_manual"):
                f_ans = questionary.text(t("builder.enter_hex"), default=flash, style=custom_style).ask()
                if f_ans: config_dict["CONFIG_FLASH_START"] = f_ans
            elif f_ans:
                config_dict["CONFIG_FLASH_START"] = f_ans.split(" (")[1].replace(")", "")
        elif ans == t("builder.edit_comm"):
            c_ans = questionary.select(t("builder.select_interface"), choices=["USB", "UART", "CAN", "SPI"], style=custom_style).ask()
            if c_ans:
                config_dict["CONFIG_USB"]    = "y" if c_ans == "USB"  else "n"
                config_dict["CONFIG_SERIAL"] = "y" if c_ans == "UART" else "n"
                config_dict["CONFIG_CANBUS"] = "y" if c_ans == "CAN"  else "n"
                config_dict["CONFIG_SPI"]    = "y" if c_ans == "SPI"  else "n"
        elif ans == t("builder.edit_clock"):
            clk = questionary.text(t("builder.enter_clock"), default=clock, style=custom_style).ask()
            if clk: config_dict["CONFIG_CLOCK_FREQ"] = clk
    # ──────────────────────────────────────────────────────────────

        
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
                
        return {"status": "error", "message": t("builder.no_binary")}
        
    except subprocess.CalledProcessError as e:
         return {"status": "error", "message": t("builder.make_error", code=e.returncode, error=e.stderr)}
    except FileNotFoundError:
         return {"status": "error", "message": t("builder.make_not_found")}
    except Exception as e:
         return {"status": "error", "message": t("builder.unexpected_error", error=str(e))}
