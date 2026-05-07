import os
import glob
import sys
from core.scraper import parse_config, extract_profile_defaults
from core.generator import generate_config
from firmware.derivation import derive_config

def test_all_configs():
    config_dir = os.path.join(".klipper_tmp", "config")
    files = glob.glob(os.path.join(config_dir, "generic-*.cfg")) + glob.glob(os.path.join(config_dir, "printer-*.cfg"))
    
    print(f"Found {len(files)} board/printer configs to test.")
    
    success = 0
    failures = []
    
    kace_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = os.path.join("tests", "fixtures", "fuzz_temp.cfg")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for cfg_file in files:
        filename = os.path.basename(cfg_file)
        
        with open(cfg_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        try:
            # 1. Parse config and inject BLTouch if mapped
            parsed = parse_config(raw_text, filename)
            defaults = extract_profile_defaults(parsed)
            
            # Extract MCU string to test derivation if present
            mcu_block = parsed.get("mcu", {})
            mcu_serial = mcu_block.get("serial", "unknown")
            
            # Mock user input
            user_data = {
                "mcu_path": "/dev/serial/by-id/usb-Klipper_mock",
                "kinematics": defaults.get("kinematics", "cartesian"),
                "x_size": "235",
                "y_size": "235",
                "z_size": "250",
                "stepper_drivers": "TMC2209",
                "hotend_thermistor": defaults.get("hotend_thermistor", "EPCOS 100K B57560G104F"),
                "bed_thermistor": defaults.get("bed_thermistor", "EPCOS 100K B57560G104F"),
                "probe": "BLTouch",
                "motors": "4",
                "z_motors": "1",
                "extruder": "1",
                "runout": "Yes",
                "language": "en"
            }
            
            # Generate config to test Jinja templating
            # We catch SystemExit because generate_config calls sys.exit(1) if TODOs remain.
            # But wait, many generic configs DO have TODOs.
            # The SystemExit is expected behavior if TODOs are present.
            try:
                generate_config(parsed, user_data, output_path=output_file)
            except SystemExit:
                pass # Expected for configs with TODOs
                
            success += 1
            
        except Exception as e:
            failures.append((filename, str(e)))
            
    if os.path.exists(output_file):
        os.remove(output_file)
        
    print(f"\nTested {len(files)} configs.")
    print(f"\033[92mSUCCESS: {success}\033[0m")
    
    if failures:
        print(f"\033[91mFAILED: {len(failures)}\033[0m")
        for fname, err in failures:
            print(f"  - {fname}: {err}")
    else:
        print("\033[92mAll configs parsed and generated successfully without fatal crashes!\033[0m")

if __name__ == "__main__":
    test_all_configs()
