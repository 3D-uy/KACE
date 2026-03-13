# KACE (Klipper Automated Configuration Ecosystem)

KACE is a Python-based automation tool designed to eliminate the manual complexity of creating a `printer.cfg`.

## Quick Start (via SSH)

If you have Git installed on your Klipper host, you can run KACE directly:

```bash
# 1. Clone the repository
git clone https://github.com/3D-uy/KACE.git
cd KACE

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the wizard
python main.py
```

## Manual Installation

1. **Download**: Click the "Download Project (.zip)" button in the KACE web portal.
2. **Upload**: Use MobaXterm's SFTP browser to drag the `kace` folder to your Pi (e.g., to `/home/pi/`).
3. **Execute**: Open an SSH terminal in MobaXterm and run `python main.py` inside the folder.

## Features
- **GitHub Scraper**: Fetches real-time pinouts from the official Klipper repo.
- **Interactive Wizard**: Auto-detects MCU serial IDs and guides you through hardware selection.
- **SSH Deployment**: Automatically push your generated `printer.cfg` to your Klipper host via SSH.
