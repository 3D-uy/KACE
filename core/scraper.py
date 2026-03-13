import urllib.request
import json
import configparser
import io

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
    Klipper configs often have inline comments without a space, or multiple same-named sections.
    We use configparser with strict=False to extract stepper, heater, and fan pins.
    """
    config = configparser.ConfigParser(allow_no_value=True, strict=False, inline_comment_prefixes=('#', ';'))
    try:
        config.read_string(raw_cfg)
    except configparser.Error:
        pass
    
    data = {}
    for section in config.sections():
        data[section] = {}
        for key, val in config.items(section):
            # Clean up inline comments from values if any slipped through
            if val and '#' in val:
                val = val.split('#')[0].strip()
            data[section][key] = val
    return data
