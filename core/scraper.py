import urllib.request
import json
import re

def fetch_config_list():
    """Fetches the list of generic and printer configs from Klipper GitHub."""
    url = "https://api.github.com/repos/Klipper3d/klipper/contents/config"
    req = urllib.request.Request(url, headers={'User-Agent': 'KACE-App'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            configs = [item['name'] for item in data if item['name'].startswith('generic-') or item['name'].startswith('printer-')]
            return configs
    except Exception as e:
        print(f"Error fetching config list: {e}")
        # Fallback to a hardcoded list if API fails (e.g., rate limit)
        return ["generic-bigtreetech-skr-v1.4.cfg", "generic-creality-v4.2.2.cfg"]

def fetch_raw_config(filename):
    """Fetches the raw content of a specific config file."""
    url = f"https://raw.githubusercontent.com/Klipper3d/klipper/master/config/{filename}"
    req = urllib.request.Request(url, headers={'User-Agent': 'KACE-App'})
    with urllib.request.urlopen(req) as response:
        return response.read().decode()

def parse_config(raw_cfg):
    """
    Parses the raw Klipper config. 
    Extracts pins even from commented-out sections (like #[tmc2208 stepper_x]).
    """
    data = {}
    current_section = None
    for line in raw_cfg.split('
'):
        line = line.strip()
        
        # Match section headers like [stepper_x] or #[tmc2208 stepper_x]
        section_match = re.match(r'^#?s*[(.*?)]', line)
        if section_match:
            current_section = section_match.group(1)
            if current_section not in data:
                data[current_section] = {}
            continue
        
        if current_section:
            # Match key-value pairs like step_pin: P2.2 or #uart_pin: P1.10
            kv_match = re.match(r'^#?s*([a-zA-Z0-9_]+)s*:s*(.*)', line)
            if kv_match:
                key = kv_match.group(1)
                val = kv_match.group(2)
                # Clean up inline comments
                if '#' in val:
                    val = val.split('#')[0].strip()
                data[current_section][key] = val
    return data
