#!/usr/bin/env python3

__version__ = "v0.1.0-beta"

import os
import sys
import time

# ── Normalize stdout/stderr to UTF-8 (critical for Windows) ──
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except (AttributeError, OSError):
    # Python < 3.7 or non-reconfigurable streams (e.g., piped output in some CI)
    pass

# ── Early argument handling (no heavy imports needed) ─────────
if len(sys.argv) > 1:
    if sys.argv[1] in ("--version", "-v"):
        print(f"KACE {__version__}")
        sys.exit(0)
    
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--dev-mcu="):
            os.environ["KACE_DEV_MCU"] = arg.split("=", 1)[1]
        elif arg == "--dev-mcu" and i + 1 < len(sys.argv):
            os.environ["KACE_DEV_MCU"] = sys.argv[i + 1]
        elif arg == "--auto":
            os.environ["KACE_AUTO"] = "1"

import questionary

if os.environ.get("KACE_AUTO") == "1":
    print("\n\033[93m[AUTO MODE]\033[0m User interactions disabled. Using safe defaults for all prompts.", flush=True)
    
    class MockQuestionary:
        def __init__(self, default_val):
            self.default_val = default_val
        def ask(self):
            return self.default_val

    def mock_select(msg, choices, default=None, **kwargs):
        val_board_type = os.environ.get("KACE_DEV_BOARD_TYPE")
        if "Select your Board:" in msg and val_board_type:
            if val_board_type in choices:
                return MockQuestionary(val_board_type)
        if not choices:
            val = default
        elif isinstance(choices[0], str):
            val = choices[0]
        elif isinstance(choices[0], dict):
            val = choices[0].get('value')
        else:
            val = getattr(choices[0], 'value', None)
        return MockQuestionary(default if default is not None else val)

    def mock_autocomplete(msg, choices, **kwargs):
        val_printer = os.environ.get("KACE_DEV_PRINTER")
        if "Select your Printer Model" in msg and val_printer:
            if val_printer in choices:
                return MockQuestionary(val_printer)
                
        val_env = os.environ.get("KACE_DEV_BOARD")
        if val_env and val_env in choices:
            return MockQuestionary(val_env)
        val = choices[0] if choices else None
        return MockQuestionary(val)

    def mock_text(msg, default="", **kwargs):
        return MockQuestionary(default)
        
    def mock_confirm(msg, default=False, **kwargs):
        return MockQuestionary(default) # Safe default: aborts builds/deployments

    def mock_password(msg, **kwargs):
        return MockQuestionary("")

    questionary.select = mock_select
    questionary.autocomplete = mock_autocomplete
    questionary.text = mock_text
    questionary.confirm = mock_confirm
    questionary.password = mock_password

from core.scraper import fetch_raw_config, parse_config
from core.wizard import run_wizard
from core.style import custom_style
from core.generator import generate_config
from core.deployer import deploy_config, deploy_usb, deploy_local, deploy_avrdude
from core.banner import print_kace_banner
from core.translations import t


def print_summary(user_data: dict):
    """Print final summary with output paths and next steps."""
    G = "\033[92m"
    Y = "\033[93m"
    C = "\033[96m"
    B = "\033[1m"
    R = "\033[0m"

    fw_path = user_data.get('firmware_path', '~/kace/klipper.bin')
    cfg_path = os.path.expanduser('~/kace/printer.cfg')

    print("")
    print(f"  {G}══════════════════════════════════════════{R}")
    print(f"  {B}{G}  ✅ {t('summary.title')}{R}")
    print(f"  {G}══════════════════════════════════════════{R}")
    print("")
    print(f"  {B}{t('summary.firmware')}{R} {Y}{fw_path}{R}")
    print(f"  {B}{t('summary.config')}{R} {Y}{cfg_path}{R}")
    print("")
    print(f"  {B}--- Generation Details ---{R}")
    print(f"  {B}Printer Profile:{R} {Y}{user_data.get('printer_profile') or 'Custom / Scratch Build'}{R}")
    print(f"  {B}Board Config:   {R} {Y}{user_data.get('board')}{R}")
    print(f"  {B}Kinematics:     {R} {Y}{user_data.get('kinematics')}{R}")
    print(f"  {B}Thermistors:    {R} {Y}{user_data.get('hotend_thermistor')} (Hotend), {user_data.get('bed_thermistor')} (Bed){R}")
    print("")
    print(f"  {B}{C}{t('summary.next_steps')}{R}")
    print(f"  {C}1.{R} {t('summary.step1')}")
    print(f"  {C}2.{R} {t('summary.step2')}")
    print(f"  {C}3.{R} {t('summary.step3')}")
    print("")
    print(f"  {G}──────────────────────────────────────────{R}")
    print("")


def main():
    print_kace_banner("Klipper Automated Configuration Ecosystem", __version__)
    
    # ── Dashboard (bypassed in CI / auto / dev modes) ─────────
    _bypassed = (
        os.environ.get("KACE_AUTO") == "1"
        or os.environ.get("KACE_DEV_MCU")
        or os.environ.get("KACE_DEV_PRINTER")
        or os.environ.get("KACE_DEV_BOARD")
        or os.environ.get("KACE_DEV_BOARD_TYPE")
    )
    if not _bypassed:
        from core.dashboard import detect_system_state, run_dashboard
        _state = detect_system_state()
        _action = run_dashboard(_state)
        if _action == "quit":
            sys.exit(0)
    
    # Milestone 3 & 4: Interactive Wizard
    try:
        user_data = run_wizard()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\033[93m{t('kace.cancelled')}\033[0m")
        sys.exit(0)
    except ImportError as e:
        print(f"\n\033[91mERROR:\033[0m {t('kace.missing_dep', error=e)}")
        print(f"\033[93m{t('kace.missing_dep_hint')}\033[0m")
        sys.exit(1)

    # ==========================================
    # PHASE 1: CONFIGURATION FETCH & DRIVER SETUP
    # ==========================================
    raw_cfg = fetch_raw_config(user_data['board'])
    parsed_data = parse_config(raw_cfg, user_data['board'])

    # --- Multi-Z Pin Verification ---
    z_motors = int(user_data.get('z_motors', 1))
    if z_motors > 1:
        available_driver_keys = sorted([k for k in parsed_data.keys() if k.startswith("extruder") and k != "extruder"])
        for i in range(2, z_motors + 1):
            motor_name = f"stepper_z{i - 1}"

            if motor_name in parsed_data:
                continue

            print(f"\n\033[96m{t('wizard.mapping_pins', motor=motor_name)}\033[0m")
            if not available_driver_keys:
                print(f"\033[93m{t('wizard.no_drivers_warning')}\033[0m")

            driver_choices = []
            for dk in available_driver_keys:
                label = dk.replace("extruder", "E")
                if dk == "extruder1":
                    label = "E1 (recommended)"
                driver_choices.append({"name": label, "value": dk})

            driver_choices.append({"name": t("choice.custom_pins"), "value": "custom"})
            driver_choices.append({"name": t("choice.quit_setup"), "value": "quit"})

            selected_driver = questionary.select(
                t("wizard.select_driver_z", motor=motor_name.upper()),
                choices=driver_choices,
                style=custom_style
            ).ask()

            if selected_driver == "quit" or selected_driver is None:
                print(f"\n\033[91m{t('kace.abort_missing_pins')}\033[0m")
                sys.exit(1)

            if selected_driver == "custom":
                print(f"\nAssigning custom pins for {motor_name}:")
                step_pin = questionary.text(t("wizard.custom_step_pin"), style=custom_style).ask()
                dir_pin = questionary.text(t("wizard.custom_dir_pin"), style=custom_style).ask()
                en_pin = questionary.text(t("wizard.custom_en_pin"), style=custom_style).ask()

                if not step_pin or not dir_pin or not en_pin:
                    print(f"\n\033[91m{t('kace.abort_valid_pins')}\033[0m")
                    sys.exit(1)

                parsed_data[motor_name] = {
                    "step_pin": step_pin,
                    "dir_pin": dir_pin,
                    "enable_pin": en_pin
                }

                driver_type = user_data.get("driver_type", "None (Standard)")
                driver_mode = user_data.get("driver_mode", "")
                if "TMC" in driver_type and driver_mode in ["UART", "SPI"]:
                    uart_pin = questionary.text(
                        t("wizard.custom_uart_pin", mode=driver_mode.lower(), motor=motor_name),
                        style=custom_style
                    ).ask()
                    if not uart_pin:
                        print(f"\n\033[91m{t('kace.abort_no_uart', mode=driver_mode)}\033[0m")
                        sys.exit(1)
                    tmc_section = f"{driver_type.lower()} {motor_name}"
                    pin_key = "uart_pin" if driver_mode == "UART" else "cs_pin"
                    parsed_data[tmc_section] = {pin_key: uart_pin, "run_current": "0.650"}
            else:
                src_data = parsed_data[selected_driver]
                parsed_data[motor_name] = {
                    "step_pin": src_data.get("step_pin", ""),
                    "dir_pin": src_data.get("dir_pin", ""),
                    "enable_pin": src_data.get("enable_pin", "")
                }

                driver_type = user_data.get("driver_type", "None (Standard)")
                driver_mode = user_data.get("driver_mode", "")
                if "TMC" in driver_type:
                    dest_tmc = f"{driver_type.lower()} {motor_name}"
                    found_tmc = False
                    for possible_tmc in ["tmc2209", "tmc2208", "tmc2130", "tmc5160", "tmc2225", "tmc2240"]:
                        src_tmc = f"{possible_tmc} {selected_driver}"
                        if src_tmc in parsed_data:
                            parsed_data[dest_tmc] = parsed_data[src_tmc].copy()
                            del parsed_data[src_tmc]
                            found_tmc = True
                            break
                    if not found_tmc and driver_mode in ["UART", "SPI"]:
                        print(f"\n\033[91m{t('kace.abort_no_tmc_map', mode=driver_mode, driver=selected_driver)}\033[0m")
                        print(f"\033[93m{t('kace.abort_generation')}\033[0m")
                        sys.exit(1)

                del parsed_data[selected_driver]
                available_driver_keys.remove(selected_driver)

    time.sleep(0.5)
    print(f"\033[92m[*]\033[0m {t('kace.fetching_cfg_done', board=user_data['board'])}")

    # ==========================================
    # PHASE 2: FIRMWARE COMPILATION & DEPLOYMENT
    # ==========================================
    mcu = user_data.get('mcu_type')
    hint = user_data.get('mcu_hint')
    if mcu or hint == "manual":
        prompt_mcu = mcu if mcu else "manually selected board"
        ans = questionary.confirm(t("kace.compile_prompt", mcu=prompt_mcu)).ask()
        if ans:
            from firmware.builder import build_firmware_orchestrator
            print(f"\n\033[91m[*]\033[0m {t('kace.compiling')}", flush=True)
            result = build_firmware_orchestrator(
                mcu_path=user_data.get('mcu_path'),
                derived_mcu=mcu,
                hint=hint,
                output_dir="~/kace"
            )

            if result.get("status") == "success":
                print(f"\033[92mSUCCESS:\033[0m {t('kace.firmware_success', path=result.get('path'))}")
                user_data['mcu_type'] = result.get('mcu')

                deploy_options = [
                    {"name": t("kace.deploy_none"),  "value": "none"},
                    {"name": t("kace.deploy_local"),  "value": "local"},
                    {"name": t("kace.deploy_usb"),    "value": "usb"},
                ]
                if result.get('firmware') == 'klipper.elf.hex':
                    deploy_options.insert(1, {"name": t("kace.deploy_avrdude"), "value": "avrdude"})

                deploy_fw = questionary.select(
                    f"\n{t('kace.deploy_firmware_prompt')}",
                    choices=deploy_options,
                    style=custom_style
                ).ask()

                if deploy_fw == "usb":
                    deploy_usb(user_data, artifact_type="firmware")
                elif deploy_fw == "local":
                    deploy_local(user_data, artifact_type="firmware")
                elif deploy_fw == "avrdude":
                    deploy_avrdude(user_data, result.get("path"), result.get("mcu"))

            else:
                print(f"\n\033[91mERROR:\033[0m {t('kace.firmware_error', message=result.get('message'))}")
    else:
        print(f"\n\033[93m{t('kace.skip_firmware')}\033[0m")

    # ==========================================
    # PHASE 3: CONFIGURATION GENERATION
    # ==========================================
    print(f"\033[91m[*]\033[0m {t('kace.generating_cfg')}", end="", flush=True)
    generate_config(parsed_data, user_data)
    time.sleep(0.5)
    print(f"\r\033[92m[*]\033[0m {t('kace.generating_cfg_done')}")
    
    cfg_path = os.path.expanduser('~/kace/printer.cfg')
    print(f"\n\033[92mSUCCESS:\033[0m {t('kace.cfg_success', path=cfg_path)}")

    # ==========================================
    # PHASE 4: CONFIGURATION DEPLOYMENT
    # ==========================================
    deploy_cfg = questionary.select(
        f"\n{t('kace.deploy_cfg_prompt')}",
        choices=[
            {"name": t("kace.deploy_none"),  "value": "none"},
            {"name": t("kace.deploy_local"),  "value": "local"},
            {"name": t("kace.deploy_usb"),    "value": "usb"},
            {"name": t("kace.deploy_ssh"),    "value": "ssh"},
        ],
        style=custom_style
    ).ask()

    if deploy_cfg == "usb":
        deploy_usb(user_data, artifact_type="config")
    elif deploy_cfg == "local":
        deploy_local(user_data, artifact_type="config")
    elif deploy_cfg == "ssh":
        user_data['host'] = questionary.text(t("kace.ssh_host_prompt"), style=custom_style).ask()
        user_data['user'] = questionary.text(t("kace.ssh_user_prompt"), default="pi", style=custom_style).ask()
        user_data['password'] = questionary.password(t("kace.ssh_pass_prompt"), style=custom_style).ask()
        user_data['dest_path'] = questionary.text(t("kace.ssh_dest_prompt"), default="~/printer_data/config/", style=custom_style).ask()
        if user_data['host'] and user_data['user'] and user_data['dest_path']:
            deploy_config(user_data)

    time.sleep(0.5)
    print_summary(user_data)
    sys.exit(0)

if __name__ == "__main__":
    main()
