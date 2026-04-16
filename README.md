<p align="center">
  <img src="docs/assets/kace_banner.png" width="1000">
</p>

<h1 align="center">🚀 KACE — Klipper Automated Configuration Ecosystem</h1>

<p align="center">
  ![CI](https://github.com/3D-uy/kace/actions/workflows/test.yml/badge.svg)
  <img src="https://img.shields.io/badge/status-beta-orange?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/version-v0.1.0--beta-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi-green?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/github/license/3D-uy/KACE?style=flat-square" alt="License">
</p>



<p align="center">
🌐 <strong>Language</strong><br>
🇺🇸 English | 🇪🇸 <a href="docs/es/README.md">Español</a> | 🇧🇷 <a href="docs/pt/README.md">Português</a>
</p>

> [!WARNING]
> **KACE is currently in Beta.** Core features are working, but you may encounter bugs or rough edges.
> Always review generated files before use. Report issues using the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template.

---

## ⚡ Install Klipper without the headaches

KACE automates the entire Klipper setup process — from hardware detection to firmware compilation and ready-to-use configuration generation.

👉 Fewer errors  
👉 Less time  
👉 More printing

---

## 🧠 What is KACE, really?

It is an **intelligent configuration and firmware engine** that:

- 🔍 Automatically detects your hardware (MCU)
- 🧠 Interprets your system without manual configuration
- ⚙️ Generates a ready-to-use `printer.cfg`
- 🔥 Automatically compiles firmware (`klipper.bin`)
- 🧭 Only guides you when necessary

---

## 🎯 Why KACE?

Setting up Klipper manually involves:

- firmware errors
- incompatible configs
- complex and confusing steps

**KACE eliminates all of that:**

- ✅ Automates complex technical decisions
- ✅ Reduces critical errors
- ✅ Works with real Klipper configurations
- ✅ Minimizes user interaction

---

## 🟡 Project Status — Beta 1

> KACE is currently in **active beta**. Core features are working, but you may encounter rough edges.

| Feature | Status |
|---|---|
| MCU Auto-detection | ✅ Working |
| GitHub Scraper | ✅ Working |
| `printer.cfg` Generation | ✅ Working |
| Firmware Compilation | ✅ Working |
| SSH Deploy | ✅ Working |
| One-line install | ✅ Working |

---

## ⚡ One-Line Install

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
```

> This will install all dependencies, clone the repository, and set up the global `kace` command automatically.

---

## 📋 Requirements

Before using KACE:

✔ Raspberry Pi Imager installed in SD card: includes **Klipper**, **Mainsail OS**, **Moonraker** (recommended)  
✔ SSH access to your Raspberry Pi (Mobaxterm) 

❌ You NO LONGER need to:

- Manually compile firmware
- Create the printer.cfg file

---

## 🧭 How it works

KACE automates the entire process:

1. 🔍 Automatically detects your MCU
2. 📦 Fetches official configurations from Klipper
3. 🧠 Suggests compatible options
4. ⚙️ Generates an optimized `printer.cfg`
5. 🔥 Compiles firmware automatically
6. 📁 Saves everything to `~/kace/`

---

## 📦 Output

After running KACE you will have:

```
~/kace/
├── printer.cfg
├── klipper.bin / klipper.uf2 / klipper.hex
```

---

## 🚀 Next Steps

1. Flash firmware to your board (SD / USB)
2. Upload `printer.cfg` to Klipper
3. Restart services:

```bash
sudo reboot
```

---

## 🛠️ Key Features

| Feature | Description |
| --- | --- |
| 🔍 **MCU Auto-detection** | Identifies your hardware automatically |
| 🧠 **Intelligent Engine** | Derives configuration without templates |
| ⚙️ **Config Generator** | Generates a clean `printer.cfg` |
| 🔥 **Firmware Builder** | Compiles firmware automatically |
| 🧪 **Pre-validation** | Catches errors before compiling |
| 🌐 **GitHub Scraper** | Uses official Klipper configurations |
| 💻 **Interactive CLI** | Simple and guided UX |

---

## 🧠 How it works (concept)

KACE uses a hybrid system:

- Automatic derivation based on MCU
- Pre-compilation validation
- Interaction only when necessary

👉 No templates  
👉 No static configurations  
👉 No external tool dependencies

---

## ⚠️ Disclaimer

KACE is an open-source tool designed to simplify Klipper configuration.

By using this software, you acknowledge that you do so **at your own risk**.  
The author assumes **no responsibility for hardware damage, misconfiguration, or unexpected behavior** resulting from the generated configuration.

👉 Always review the generated `printer.cfg` before using your printer.  
👉 Verify firmware before flashing.

---

## 🗑️ Uninstall

To remove KACE from your system:

```bash
# Remove the global command symlink
sudo rm -f /usr/local/bin/kace

# Or if installed without sudo (fallback)
rm -f ~/.local/bin/kace

# Remove the KACE directory
rm -rf ~/kace
```

---

## 🎬 Full Guides

👉 Complete documentation:

* 🇺🇸 English:   *(this page)*
* 🇪🇸 Español:   <a href="docs/es/README.md">README.md</a>
* 🇧🇷 Português: <a href="docs/pt/README.md">README.md</a>

👉 Pi Imager Setup:
* 🇺🇸 English:   <a href="docs/en/pi_imager.md">pi_imager.md</a>
* 🇪🇸 Español:   <a href="docs/es/pi_imager.md">pi_imager.md</a>
* 🇧🇷 Português: <a href="docs/pt/pi_imager.md">pi_imager.md</a>

👉 Full Klipper Install:
* 🇺🇸 English:   <a href="docs/en/Klipper_install.md">Klipper_install.md</a>
* 🇪🇸 Español:   <a href="docs/es/klipper_install.md">klipper_install.md</a>
* 🇧🇷 Português: <a href="docs/pt/Klipper_install.md">Klipper_install.md</a>


---

## 🙌 Contribute & Feedback

KACE evolves with the community:

* 🐛 Report bugs
* 💡 Suggest improvements
* 🤝 Contribute code

👉 Every contribution counts.

---

## 🙏 Acknowledgments

This project builds on the incredible work of the **Klipper** community.

KACE aims to make that ecosystem more accessible for everyone.

---

## 📜 License & Usage

KACE is licensed under GPL-3.0 🛠️

💡 For commercial use, distribution in paid products, or rebranding,  
please contact the author.

🏷️ The "KACE" name and branding may not be used in commercial products  
without permission from the author.

🤝 Attribution is appreciated and helps support the project.

---

<p align="center">

⭐ If you like this project, give it a star  
🚀 Built to simplify Klipper

</p>
