import urllib.request
import json
import re
import os
import time

def fetch_config_list():
    """Fetches the list of generic and printer configs from Klipper GitHub."""
    cache_file = os.path.expanduser("~/.kace_boards_cache.json")
    
    # 1. Check persistent cache first (valid for 3 days)
    try:
        if os.path.exists(cache_file):
            if time.time() - os.path.getmtime(cache_file) < 3 * 24 * 3600:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)
                    if configs:
                        return configs
    except Exception:
        pass

    # 2. Try GitHub API
    url = "https://api.github.com/repos/Klipper3d/klipper/contents/config"
    req = urllib.request.Request(url, headers={'User-Agent': 'KACE-App'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            configs = [item['name'] for item in data if item['name'].startswith('generic-') or item['name'].startswith('printer-')]
            
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(configs, f)
            except Exception: pass
            
            return configs
    except Exception as api_err:
        # 3. API Limit hit, fallback to scraping GitHub HTML tree
        try:
            tree_url = "https://github.com/Klipper3d/klipper/tree/master/config"
            req_html = urllib.request.Request(tree_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) KACE-App'})
            with urllib.request.urlopen(req_html) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Extract from React JSON payload or standard hrefs
                matches = re.findall(r'"name":"((?:generic|printer)-[^"]+\.cfg)"', html)
                matches_url = re.findall(r'href="/Klipper3d/klipper/blob/[^/]+/config/((?:generic|printer)-.*?\.cfg)"', html)
                configs = list(set(matches + matches_url))
                
                if configs:
                    configs = sorted(configs)
                    try:
                        with open(cache_file, 'w', encoding='utf-8') as f:
                            json.dump(configs, f)
                    except Exception: pass
                    return configs
        except Exception:
            pass
            
        # 4. Try expired cache as last resort
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)
                    if configs:
                        return configs
        except Exception:
            pass

        print(f"\n\033[93mWarning: Error fetching config list from GitHub ({api_err}). Falling back to manual entry.\033[0m")
        return ["generic-bigtreetech-skr-v1.4.cfg", "generic-creality-v4.2.2.cfg"]

def fetch_raw_config(filename):
    """Fetches the raw content of a specific config file."""
    url = f"https://raw.githubusercontent.com/Klipper3d/klipper/master/config/{filename}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 KACE-App'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8', errors='ignore')

def parse_config(raw_cfg, filename=""):
    """
    Parses the raw Klipper config. 
    Extracts pins even from commented-out sections (like #[tmc2208 stepper_x]).
    """
    data = {}
    current_section = None
    last_key = None
    for raw_line in raw_cfg.split('\n'):
        line = raw_line.strip()
        if not line: continue
        
        # Match section headers like [stepper_x] or #[tmc2208 stepper_x]
        section_match = re.match(r'^#?\s*\[(.*?)\]', line)
        if section_match:
            current_section = section_match.group(1).strip().lower()
            if current_section not in data:
                data[current_section] = {}
            last_key = None
            continue
        
        if current_section:
            # Match key-value pairs like step_pin: P2.2 or #uart_pin: P1.10
            kv_match = re.match(r'^#?\s*([a-zA-Z0-9_]+)\s*:\s*(.*)', line)
            if kv_match:
                key = kv_match.group(1).strip().lower()
                val = kv_match.group(2).strip()
                
                # Prevent [board_pins] parser leakage: 'aliases' uniquely belongs to board_pins
                if key == 'aliases' and current_section != 'board_pins':
                    current_section = 'board_pins'
                    if current_section not in data:
                        data[current_section] = {}
                        
                # Clean up inline comments
                if '#' in val and key != 'aliases':
                    val = val.split('#')[0].strip()
                    
                data[current_section][key] = val
                last_key = key
            elif last_key == 'aliases':
                clean_val = line
                if clean_val.startswith('#'):
                    stripped = clean_val.lstrip('#').strip()
                    if '=' in stripped:
                        clean_val = stripped
                    else:
                        clean_val = '# ' + stripped
                        
                if clean_val and "TODO" in clean_val:
                    # Filter out individual EXP1/EXP2 mappings containing TODO
                    parts = []
                    for p in clean_val.split(','):
                        p_strip = p.strip()
                        if "TODO" in p_strip and ("EXP" in p_strip):
                            continue
                        if p_strip:
                            parts.append(p_strip)
                    if parts:
                        clean_val = ', '.join(parts) + (',' if clean_val.rstrip().endswith(',') else '')
                    else:
                        clean_val = ""
                        
                if clean_val:
                    data[current_section][last_key] += '\n    ' + clean_val
                
    # Inject known BLTouch pins for popular boards if missing
    if "bltouch" not in data:
        data["bltouch"] = {}
        
    fname = filename.lower()
    if "skr-v1.4" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^P0.10"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "P2.0"
    elif "skr-v1.3" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^P1.27"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "P2.0"
    elif "skr-mini-e3-v2.0" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^PC14"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "PA1"
    elif "skr-mini-e3-v3.0" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^PC14"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "PA1"
    elif "creality-v4.2.2" in fname or "creality-v4.2.7" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^PB1"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "PB0"
    elif "mks-gen-l" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^D18"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "D11"
    elif "mks-sgen-l" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^P1.27"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "P2.0"
    elif "mks-robin-nano" in fname:
        if "sensor_pin" not in data["bltouch"]: data["bltouch"]["sensor_pin"] = "^PA11"
        if "control_pin" not in data["bltouch"]: data["bltouch"]["control_pin"] = "PA8"
        
    return data
