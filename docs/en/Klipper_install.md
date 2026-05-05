# 🚀 KLIPPER easy installation

![Firmware](https://img.shields.io/badge/Firmware-Klipper-orange)
![Board](https://img.shields.io/badge/Board-SKR%201.4%20%2F%201.4%20Turbo-blue)
![Raspberry](https://img.shields.io/badge/Raspberry-Pi%203B-red)
![Interface](https://img.shields.io/badge/UI-Mainsail-purple)
![Guide](https://img.shields.io/badge/Guía-Instalación%20simple-success)

# 🧠 The ultimate guide to installing Klipper

This tutorial is designed to be followed along with the video.
Simply copy each block of code and paste it into the terminal.
You don’t need to type commands manually.

---

# 📋 REQUIREMENTS

* 🧠 Raspberry Pi (as an example we will use a Raspberry Pi 3B)
* 🧩 Example board: SKR 1.4 Turbo
* 💾 Good quality SD card for the Raspberry
* 💾 SD card to load firmware on the SKR
* 🔌 USB cable between Raspberry and SKR
* 💻 Windows PC
* 🖥️ MobaXterm installed

## 🔗 All links can be found below

---

# 💿 PART 1 — Flash MainsailOS to the SD card

Before starting, you need to flash the operating system onto the Raspberry Pi SD card.

We will use **Raspberry Pi Imager**, the official tool.

📥 Download here

Official website [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

Install and open the program.

Then follow these steps:

1. Click on **Raspberry Pi Model**

2. Select:

   ## Other specific-purpose OS

3. Then select:

   ## 3D printing

4. Choose:

   ## Mainsail OS

5. Click on **Choose Storage**

6. Select your **SD card**

7. Press **FINISH**

The program will download the image and flash it automatically.

# 📥 Meanwhile download the following program

## 🖥️ Download MobaXterm

Official website
[https://mobaxterm.mobatek.net/download.html](https://mobaxterm.mobatek.net/download.html)

---

# ⚡ When finished

1. Remove the SD card
2. Insert it into the **Raspberry Pi**
3. Power on the Raspberry

## Wait approximately **1 to 2 minutes** for the system to fully boot.

---

# 📡 PART 2 — Open MainsailOS

### Open your browser and go to:

```
klipper.local
```

If Mainsail opens → perfect.

---

# 🔐 PART 3 — Connect via SSH with MobaXterm

### 🖥️ Open MobaXterm → Session → SSH

Remote host:

```
klipper.local
```

Username:

```
pi
```

Password:

```
raspberry
```

## If you can log in → you are inside the Raspberry.

---

# 🔄 PART 4 — Update the system (VERY IMPORTANT)

MainsailOS already comes with Klipper, Moonraker and Mainsail installed.
The first thing we must do is update everything.

### STEP 1

In MobaXterm (connected via SSH), copy and paste:

```
sudo apt update
sudo apt upgrade -y
```

### STEP 2

Install Python:

```
sudo apt install python3-pip -y
```

### STEP 3

Update Klipper:

```
cd ~/klipper
git pull
```

### STEP 4

Reboot the Raspberry:

```
sudo reboot
```

# Wait 1–2 minutes before continuing.

## Press R to reconnect the terminal, it will ask again for user and password.

user:

```
pi
```

password:

```
raspberry
```

---

# 🧰 PART 5 — Install KIAUH

## KIAUH installation

Official site: ([https://github.com/dw-0/kiauh](https://github.com/dw-0/kiauh))

## Step 1

To download this script you need **git** installed.
If you don’t have it or are not sure, run:

```
sudo apt-get update && sudo apt-get install git -y
```

## Step 2

Once **git** is installed, download KIAUH to your *home* directory:

```
cd ~ && git clone https://github.com/dw-0/kiauh.git
```

## Step 3

Start KIAUH with:

```
./kiauh/kiauh.sh
```

---

# ⚙️ PART 6 — Compile firmware using KIAUH

In the menu select:

## 4 → Advanced

## 1 → Build

Configure as follows:

## Micro-controller Architecture:

### LPC176x

#----------------------------------------------------------#

## Processor model:

### LPC1768 (SKR 1.4)

### LPC1769 (SKR 1.4 TURBO)

#----------------------------------------------------------#

## Bootloader offset:

### 16KiB bootloader

#----------------------------------------------------------#

## Communication interface:

### USB

#----------------------------------------------------------#

### Press **Q** to exit and it will ask to save.

### Press **Y** to confirm and build the firmware.

#----------------------------------------------------------#

The firmware will be generated at:

```
/home/pi/klipper/out/klipper.bin
```

---

# 💾 PART 7 — Flash the SKR (from MobaXterm)

1. Go to:

```
/home/pi/klipper/out/
```

2. Download **klipper.bin**
3. Rename it to:

## firmware.bin (for SKR boards)

4. Copy **firmware.bin** to the SKR SD card
5. Insert the SD into the SKR
6. Power on the printer

## If the file changes to FIRMWARE.CUR → flashing was successful.

---

# 🧠 PART 8 — Install KACE

[https://github.com/3D-uy/kace](https://github.com/3D-uy/kace)

### Connect USB between Raspberry and SKR

### Power on the printer

In terminal:

## ⚡ Quick Start (via SSH)

To download this script, you need **git** installed.
If not, run:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

Run KACE directly on your Klipper host with:

## # 1

* Clone the repository
* Install dependencies (with modern OS bypass)
* Launch the ecosystem

```bash
git clone https://github.com/3D-uy/KACE.git kace
cd kace
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

## # 2

* Download the newly created **printer.cfg** and upload it to Klipper

## # 3

* Reboot the system via SSH

```
sudo reboot
```

## Restart the printer and the Raspberry

### MainsailOS should now be running on your Raspberry and

### you should find the **printer.cfg** file in the MACHINE section.

# 🎉 HAPPY PRINTING!

Your printer should now be running Klipper and you’re ready to start tuning and creating macros.
