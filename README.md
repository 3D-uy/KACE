# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automation-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[Español (ES)](README_ES.md) | [Português (BR)](README_BR.md)

KACE is a high-performance automation tool designed to eliminate the manual complexity of creating a `printer.cfg`. It bridges the gap between raw hardware and a perfectly tuned Klipper installation.

---

## ⚡ Quick Start (via SSH)

To download this script, it is necessary to have **git** installed.
If you do not have it installed or are not sure, run the following command:

```bash
sudo apt-get update && sudo apt-get install git -y
```

Run KACE directly on your Klipper host with these optimized commands:

```bash
# 1. Clone the repository
git clone https://github.com/3D-uy/KACE.git
cd KACE

# 2. Install dependencies (with modern OS bypass)
pip3 install -r requirements.txt --break-system-packages

# 3. Launch the Ecosystem
python3 main.py
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

## 📦 Manual Installation

1. **Download**: Click **"Download Project (.zip)"** in the KACE portal.
2. **Upload**: Drag the `kace` folder to your Pi via MobaXterm SFTP.
3. **Execute**: Run `python3 main.py` in the terminal.

---

*Developed for the Klipper Community.*
