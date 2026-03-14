<p align="center">
  <img src="assets/kace_banner2.png" width="800">
</p>

# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automation-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[Español (ES)](README_ES.md) | [Português (BR)](README_BR.md)

### KACE automatically generates a working Klipper printer.cfg
### by detecting your hardware and guiding you through configuration.

## 🟢 Why KACE?

Configuring Klipper can be complex for new users.

KACE simplifies the process by:
- Detecting your MCU automatically
- Suggesting compatible boards
- Guiding you through configuration
- Generating a ready-to-use printer.cfg
- Deploying it directly to your printer host

---

## ⚡ Quick Start (via SSH)

To download this script, it is necessary to have **git** installed.  
If you do not have it installed or are not sure, run the following command:

```bash
sudo apt-get update && sudo apt-get install git -y
```

Run KACE directly on your Klipper host with these optimized commands:

## 1. 
  - Clone the repository
  - Install dependencies (with modern OS bypass)
  - Launch the Ecosystem
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 KACE.py
```

---

## 🛠️ Key Features

| Feature | Description |
| :--- | :--- |
| **GitHub Scraper** | Fetches real-time pinouts directly from the official Klipper source. |
| **Smart Wizard** | Auto-detects MCU serial IDs and guides you through hardware selection. |
| **SSH Deployer** | Automatically push your generated config to the host via secure SSH. |
| **Jinja2 Engine** | Generates clean, modular, and well-commented configurations. |

---

*Developed for the Klipper Community.*
