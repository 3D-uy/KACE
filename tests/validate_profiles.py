import os
import subprocess
import shutil
import sys

# Ensure KACE core modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
        
    PROFILES_TO_TEST = [
        "printer-creality-ender3-v2-2020.cfg",
        "printer-voron2.4-250-2020.cfg",  # Correct voron name
        "printer-prusa-i3-mk3s-2021.cfg",
        "printer-artillery-sidewinder-x1-2020.cfg",
        "printer-elegoo-neptune-2-2021.cfg",
        "printer-flsun-super-racer-2021.cfg",
        "printer-kossel-2015.cfg",
        "printer-biqu-b1-2020.cfg",
        "printer-sovol-sv01-2020.cfg",
        "printer-two-trees-sapphire-plus-2020.cfg"
    ]
    
    OVERRIDE_BOARD = "generic-bigtreetech-skr-mini-e3-v3.0.cfg"
    EXPECTED_OVERRIDE_PIN = "PB13" # SKR Mini E3 V3 X-stepper pin
    
    print(f"Starting KACE End-to-End Profile Validation for {len(PROFILES_TO_TEST)} profiles...\n")
    
    results_dir = os.path.join(os.path.dirname(__file__), "results_profiles")
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)
    
    kace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kace_py = os.path.join(kace_root, "kace.py")
    python_cmd = sys.executable
    
    success_count = 0
    total_tests = 0
    failures = []
    
    for profile in PROFILES_TO_TEST:
        for mode in ["Stock", "Override"]:
            total_tests += 1
            test_name = f"{profile} [{mode}]"
            print("=======================================")
            print(f"Testing: {test_name}")
            print("=======================================")
            
            env = os.environ.copy()
            env["KACE_DEV_MCU"] = "mock"
            env["KACE_AUTO"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            env["KACE_DEV_PRINTER"] = profile
            
            if mode == "Stock":
                env["KACE_DEV_BOARD_TYPE"] = "Stock Board (from printer profile)"
            else:
                env["KACE_DEV_BOARD_TYPE"] = "Search manually..."
                env["KACE_DEV_BOARD"] = OVERRIDE_BOARD
            
            result = subprocess.run(
                [python_cmd, kace_py, "--auto"], 
                cwd=kace_root, 
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            expected_cfg = os.path.expanduser("~/kace/printer.cfg")
            passed = True
            error_reasons = []
            
            if result.returncode != 0:
                passed = False
                error_reasons.append(f"KACE crashed with return code {result.returncode}")
                
            if not os.path.exists(expected_cfg):
                passed = False
                error_reasons.append("printer.cfg was not generated at the expected location.")
            else:
                with open(expected_cfg, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                if "[mcu]" not in content:
                    passed = False
                    error_reasons.append("Missing [mcu] section in generated config.")
                if "[printer]" not in content:
                    passed = False
                    error_reasons.append("Missing [printer] section in generated config.")
                if "[stepper_x]" not in content and "[stepper_a]" not in content:
                    passed = False
                    error_reasons.append("Missing [stepper_x] or [stepper_a] (delta) section.")
                if "[extruder]" not in content:
                    passed = False
                    error_reasons.append("Missing [extruder] section.")
                    
                if "rotation_distance:" not in content:
                    passed = False
                    error_reasons.append("Missing rotation_distance parameters.")
                if "sensor_type:" not in content:
                    passed = False
                    error_reasons.append("Missing sensor_type parameters.")
                    
                # Explicit override MCU verification via pins
                if mode == "Override":
                    if EXPECTED_OVERRIDE_PIN not in content:
                        passed = False
                        error_reasons.append(f"Override pin '{EXPECTED_OVERRIDE_PIN}' not found in output. Board override failed!")
                
                # Archive the result
                dest = os.path.join(results_dir, f"{profile.replace('.cfg', '')}_{mode.lower()}.cfg")
                shutil.copy(expected_cfg, dest)
                os.remove(expected_cfg)
                
            if passed:
                print(f"\033[92m[PASS]\033[0m Successfully validated {test_name}")
                success_count += 1
            else:
                print(f"\033[91m[FAIL]\033[0m Validation failed for {test_name}:")
                for reason in error_reasons:
                    print(f"  - {reason}")
                failures.append((test_name, error_reasons))
                
                if result.stderr:
                    print(f"\nSTDERR:\n{result.stderr.strip()[-500:]}")
            print("\n")

    print("=======================================")
    print("END-TO-END PROFILE VALIDATION SUMMARY")
    print("=======================================")
    print(f"Total Tested: {total_tests}")
    print(f"\033[92mPasses: {success_count}\033[0m")
    
    if failures:
        print(f"\033[91mFailures: {len(failures)}\033[0m\n")
        for test, reasons in failures:
            print(f"  \033[93m{test}:\033[0m")
            for r in reasons:
                print(f"    - {r}")
        sys.exit(1)
    else:
        print("\033[92mAll profile combination scenarios passed successfully.\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
