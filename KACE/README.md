# KACE (Klipper Automated Configuration Ecosystem)

KACE is a Python-based automation tool designed to eliminate the manual complexity of creating a `printer.cfg`.

## Quick Start (via SSH)

If you have Git installed on your Klipper host, you can run KACE directly. 

**Note for Raspberry Pi users:** Use `python3` and `pip3` instead of `python` and `pip`.

```bash
# 1. Clone the repository
git clone https://github.com/3D-uy/KACE.git
cd KACE

# 2. If your files are in a subfolder, go into it:
# (Check with 'ls' if you see another KACE folder)
cd KACE 

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Run the wizard
python3 main.py
```

*If `pip3` is missing, install it first: `sudo apt update && sudo apt install python3-pip -y`*

## Manual Installation

1. **Download**: Click the "Download Project (.zip)" button in the KACE web portal.
2. **Upload**: Use MobaXterm's SFTP browser to drag the `kace` folder to your Pi (e.g., to `/home/pi/`).
3. **Execute**: Open an SSH terminal in MobaXterm and run `python main.py` inside the folder.

## Features
- **GitHub Scraper**: Fetches real-time pinouts from the official Klipper repo.
- **Interactive Wizard**: Auto-detects MCU serial IDs and guides you through hardware selection.
- **SSH Deployment**: Automatically push your generated `printer.cfg` to your Klipper host via SSH.
