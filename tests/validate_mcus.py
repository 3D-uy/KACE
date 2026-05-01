import os
import subprocess
import shutil
import sys

# Ensure KACE core modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.scraper import fetch_config_list

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
        
    print("Extracting configuration list from Klipper...")
    all_configs = fetch_config_list()
    # Filter for all generic Klipper configurations mapped by the scraper
    BOARDS_TO_TEST = [cfg for cfg in all_configs if cfg.startswith("generic-")]
    
    print(f"Starting KACE Automated Validation for {len(BOARDS_TO_TEST)} generic boards...\n")
    
    # Ensure tests/results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)
    
    # Store old kace working dir
    kace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kace_py = os.path.join(kace_root, "kace.py")
    
    success_count = 0
    failure_categories = {
        "Missing Pins (Unresolved TODOs)": [],
        "Missing Core Sections": [],
        "Script Crashes / Exceptions": [],
        "Unknown Generator Failures": []
    }
    
    for board in BOARDS_TO_TEST:
        print("=======================================")
        print(f"Testing Board: {board}")
        print("=======================================")
        
        # We need to simulate the environment
        env = os.environ.copy()
        env["KACE_DEV_MCU"] = "mock" # Skip MCU-based suggested list to trigger autocomplete
        env["KACE_DEV_BOARD"] = board # Force autocomplete to select this board
        env["KACE_AUTO"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        
        # Note: Depending on the OS, we invoke python3 or python.
        python_cmd = sys.executable
        
        # Run KACE
        result = subprocess.run(
            [python_cmd, kace_py, "--auto"], 
            cwd=kace_root, 
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        # Check standard config output path
        expected_cfg = os.path.expanduser("~/kace/printer.cfg")
        
        passed = True
        error_reasons = []
        is_todo_error = "unresolved 'TODO' values" in (result.stdout or "")
        
        if result.returncode != 0:
            passed = False
            error_reasons.append(f"KACE crashed with return code {result.returncode}")
        
        if not os.path.exists(expected_cfg):
            passed = False
            error_reasons.append("printer.cfg was not generated at the expected location.")
        else:
            # Parse it for fundamental sections
            with open(expected_cfg, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "[mcu]" not in content:
                passed = False
                error_reasons.append("Missing [mcu] section in generated config.")
            if "[printer]" not in content:
                passed = False
                error_reasons.append("Missing [printer] section in generated config.")
            if "[stepper_x]" not in content:
                passed = False
                error_reasons.append("Missing [stepper_x] section in generated config.")
            
            # Archive the result
            dest = os.path.join(results_dir, f"printer_{board}")
            shutil.copy(expected_cfg, dest)
            os.remove(expected_cfg) # clean up so we don't bleed into next run
            
        if passed:
            print(f"\033[92m[PASS]\033[0m Successfully validated {board}")
            success_count += 1
        else:
            print(f"\033[91m[FAIL]\033[0m Validation failed for {board}:")
            # Categorize the failure
            if is_todo_error:
                import re
                todos = re.findall(r"TODO_FOUND:\s*(.*)", result.stdout or "")
                if todos:
                    # Create a specific signature for grouping (e.g. "Missing: [bltouch]->sensor_pin")
                    signature = "Missing: " + ", ".join(sorted(list(set(todos))))
                    if signature not in failure_categories:
                        failure_categories[signature] = []
                    failure_categories[signature].append(board)
                else:
                    if "Missing Pins (Unresolved TODOs)" not in failure_categories:
                        failure_categories["Missing Pins (Unresolved TODOs)"] = []
                    failure_categories["Missing Pins (Unresolved TODOs)"].append(board)
                    
            elif any(e.startswith("Missing [") for e in error_reasons):
                if "Missing Core Sections" not in failure_categories: failure_categories["Missing Core Sections"] = []
                failure_categories["Missing Core Sections"].append(board)
            elif result.returncode != 0 and result.stderr.strip():
                if "Script Crashes / Exceptions" not in failure_categories: failure_categories["Script Crashes / Exceptions"] = []
                failure_categories["Script Crashes / Exceptions"].append(board)
            else:
                if "Unknown Generator Failures" not in failure_categories: failure_categories["Unknown Generator Failures"] = []
                failure_categories["Unknown Generator Failures"].append(board)
                
            for reason in error_reasons:
                print(f"  - {reason}")
            # Optionally print standard error from process
            if result.stderr:
                clean_stderr = result.stderr.strip()[-500:]
                print(f"\nSTDERR:\n{clean_stderr}")
            if result.stdout and not is_todo_error:
                clean_stdout = result.stdout.strip()[-1000:]
                print(f"\nSTDOUT:\n{clean_stdout}")
            
        print("\n")

    print("=======================================")
    print("MCU VALIDATION SUMMARY")
    print("=======================================")
    print(f"Total Tested: {len(BOARDS_TO_TEST)}")
    print(f"\033[92mPasses: {success_count}\033[0m")
    
    total_failures = sum(len(fails) for fails in failure_categories.values())
    if total_failures > 0:
         print(f"\033[91mFailures: {total_failures}\033[0m\n")
         print("Failure Breakdown by Category:")
         for category, boards in failure_categories.items():
            if boards:
                print(f"  \033[93m{category} ({len(boards)}):\033[0m")
                for b in boards:
                    print(f"    - {b}")
         sys.exit(1)
    else:
         print("\033[92mAll tests passed successfully.\033[0m")
         sys.exit(0)

if __name__ == "__main__":
    main()
