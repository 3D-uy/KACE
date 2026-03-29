<p align="center">
  <img src="assets/kace_banner.png" width="1000">
</p>

# 🚀 KACE — Klipper Automated Configuration Ecosystem

<p align="center">

🌐 **Language**  
🇺🇸 English | 🇪🇸 <a href="installs/es/README.md">Español</a> | 🇧🇷 <a href="installs/pt/README.md">Português</a>

</p>

---

### ⚡ Install Klipper the easy way — just copy, paste, and go.

KACE automatically generates a fully functional **Klipper `printer.cfg`** by detecting your hardware and guiding you through a smart configuration process.

---

## 🎯 Why KACE?

Setting up Klipper can be complex and time-consuming, especially for new users.

**KACE simplifies everything:**

- 🔍 Automatically detects your MCU
- 🧠 Suggests compatible boards
- 🧭 Guides you step-by-step
- ⚙️ Generates a ready-to-use `printer.cfg`

---

## ⚠️ Disclaimer

KACE is provided as an open-source tool intended to simplify the creation of a Klipper configuration.

By using this software, you acknowledge that you are doing so **at your own risk**.  
The author assumes **no responsibility for potential hardware damage, misconfiguration, or unexpected behavior** resulting from the generated configuration.

👉 Always review and verify the generated `printer.cfg` before running your printer.

---

## 📋 Prerequisites

Before using **KACE**, make sure the following steps are completed:

✔ Raspberry Pi SD card flashed using **Raspberry Pi Imager** with **Mainsail OS**  
✔ Klipper, Moonraker, and Mainsail are running  
✔ **KIAUH** is installed  
✔ Firmware compiled using KIAUH  
✔ Firmware flashed to your printer control board  

Once ready, KACE will handle the rest.

---

## ⚡ Quick Start (via SSH)

Make sure `git` is installed:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
````

---

### 🚀 Run KACE

```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

---

### 📥 Next Steps

1. Download the generated `printer.cfg`
2. Upload it to your Klipper interface
3. Restart services:

```bash
sudo reboot
```

---

## 🛠️ Key Features

| Feature               | Description                                             |
| :-------------------- | :------------------------------------------------------ |
| 🔎 **GitHub Scraper** | Fetches real-time pinouts from official Klipper sources |
| 🧠 **Smart Wizard**   | Detects MCU and guides hardware selection               |
| 🔐 **SSH Deployer**   | Pushes configs directly to your host                    |
| ⚙️ **Jinja2 Engine**  | Generates clean, modular, and readable configs          |

---

## 🎬 Full Installation Guide

👉 Step-by-step guide available here:

* 🇺🇸 English: *(coming soon / or add link)*
* 🇪🇸 Español: `Klipper Install/Klipper_install_es.md`
* 🇧🇷 Português: *(add when ready)*

---

## 🙌 Contribute & Feedback

KACE is evolving, and your feedback is key.

* 🐛 Report issues
* 💡 Suggest improvements
* 🤝 Contribute ideas

👉 Every bit of feedback helps improve the project.

---

## 🙏 Acknowledgments

KACE would not exist without the incredible work of the **Klipper** and **KIAUH** communities.

Their dedication and open-source spirit made advanced 3D printing accessible to thousands of users.

KACE is built to give something back — making Klipper easier for everyone.

---

<p align="center">

⭐ If you like this project, consider giving it a star
🚀 Built for the Klipper community

</p>


