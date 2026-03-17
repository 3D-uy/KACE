<p align="center">
  <img src="assets/kace_banner2.png" width="1000">
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

---

## ⚠️ Disclaimer

KACE is provided as an open-source tool intended to simplify the creation of a Klipper configuration.

By using this software, you acknowledge that you are doing so **at your own risk**.  
The author assumes **no responsibility for potential hardware damage, misconfiguration, or unexpected behavior** resulting from the generated configuration.

Always review and verify the generated `printer.cfg` before running your printer.


## 📋 Prerequisites

Before using **KACE**, make sure the following steps are already completed:

✔ The Raspberry Pi SD card has been flashed using **Raspberry Pi Imager** with **MainsailOS**

✔ Klipper, Moonraker and Mainsail are running on the Raspberry Pi

✔ **KIAUH** has been installed on the Raspberry Pi

✔ The printer firmware has been compiled using KIAUH  

✔ The compiled firmware has been flashed to your printer control board

Once these steps are completed, you can use **KACE** to generate a clean and structured `printer.cfg`.

---

## ⚡ Quick Start (via SSH)

To download this script, it is necessary to have **git** installed.  
If you do not have it installed or are not sure, run the following command:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

Run KACE directly on your Klipper host with these optimized commands:

## # 1. 
  - Clone the repository
  - Install dependencies (with modern OS bypass)
  - Launch the Ecosystem
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

## # 2.

  -Download the printer.cfg file just created and upload it to Klipper.

## # 3. 

  -Restart system from SSH
  
```
sudo systemctl restart klipper moonraker
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

## 🙏 Acknowledgments

KACE would not exist without the incredible work of the **Klipper** and **KIAUH** communities.

Their dedication, innovation, and open-source spirit have made advanced 3D printing accessible to thousands of users around the world.

KACE was created to contribute back to this ecosystem by making the initial setup easier and more approachable for new Klipper users.

*Developed for the Klipper Community.*
