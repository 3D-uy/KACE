# 🚀 KLIPPER instalación fácil

![Firmware](https://img.shields.io/badge/Firmware-Klipper-orange)
![Board](https://img.shields.io/badge/Board-SKR%201.4%20%2F%201.4%20Turbo-blue)
![Raspberry](https://img.shields.io/badge/Raspberry-Pi%203B-red)
![Interface](https://img.shields.io/badge/UI-Mainsail-purple)
![Guide](https://img.shields.io/badge/Guía-Instalación%20simple-success)

<p align="center">

🌐 **Idioma**  
🇺🇸 <a href="../../klipper_install.md">English</a> | 🇪🇸 Español | 🇧🇷 <a href="../pt/klipper_install.md">Português</a>

</p>


# 🧠 La guía definitiva para instalar Klipper

Este tutorial está diseñado para seguirse junto con el video.  
Simplemente copia cada bloque de código y pégalo en la terminal.  
No necesitas escribir comandos manualmente.

---

# 📋 REQUISITOS

- 🧠 Raspberry Pi (como ejemplo usaremos una Raspberry Pi 3B)
- 🧩 Placa ejemplo: SKR 1.4 Turbo
- 💾 Tarjeta SD de buena calidad para la Raspberry
- 💾 Tarjeta SD para cargar firmware en la SKR
- 🔌 Cable USB entre Raspberry y SKR
- 💻 PC con Windows
- 🖥️ MobaXterm instalado

## 🔗 Todos los links los encontrarás más abajo

---

# 💿 PARTE 1 — Grabar MainsailOS en la tarjeta SD

Antes de empezar necesitas grabar el sistema operativo en la tarjeta SD de la Raspberry Pi.

Usaremos **Raspberry Pi Imager**, la herramienta oficial.

📥 Descargar aquí  

  Sitio oficial https://www.raspberrypi.com/software/
  Guia para instalar **Raspberry Pi Imager**
  <a href="pi_imager.md">

  Instalar y abrir el programa.

Luego seguir estos pasos:

1. Hacer clic en **Modelo de Raspberry Pi**
2. Seleccionar:

   ## Other specific-purpose OS

3. Luego seleccionar:

   ## 3D printing

4. Elegir:

   ## Mainsail OS

5. Hacer clic en **Choose Storage**
6. Seleccionar tu **tarjeta SD**
7. Presionar **FINALIZAR**

El programa descargará la imagen y la grabará automáticamente.

# 📥 Mientras tanto descarga el siguiente programa

## 🖥️ Descargar MobaXterm

   Sitio oficial  
   https://mobaxterm.mobatek.net/download.html

---

# ⚡ Cuando termine

1. Retirar la tarjeta SD
2. Insertarla en la **Raspberry Pi**
3. Encender la Raspberry

  ## Esperar aproximadamente **1 a 2 minutos** para que el sistema arranque completamente.


# 📡 PARTE 2  Abrir MainsailOs.

### Abrir el navegador y entrar en:
```
klipper.local
```
Si abre Mainsail → perfecto.

---

# 🔐 PARTE 3 — Conectarse por SSH con MobaXterm

### 🖥️ Abrir MobaXterm → Session → SSH

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
## Si entra → estamos dentro de la Raspberry.

---

# 🔄 PARTE 4 — Actualizar el sistema (MUY IMPORTANTE)

MainsailOS ya trae Klipper, Moonraker y Mainsail instalados.
Lo primero que debemos hacer es actualizar todo.

### PASO 1

  En MobaXterm (conectado por SSH) copiar y pegar:

```
sudo apt update
sudo apt upgrade -y
```

### PASO 2

  Instalar python:

```
sudo apt install python3-pip -y
```

### PASO 3

  Actualizar Klipper:

```
cd ~/klipper
git pull
```
  
### PASO 4

  Reiniciar la Raspberry:

```
sudo reboot
```

# Esperar 1 o 2 minutos antes de continuar.

## Presionar R para reiniciar la terminal, te volverá a pedir el usuarior y el password.

user:
```
pi
```
password:
```
raspberry
```

---

Tal cual… bien visto 😏👌
Ahí KACE se está robando todo el show, no tiene sentido separarlo.

Te dejo la versión ajustada, más limpia y directa 👇

---

# ⚡ PARTE 5 — Instalar y usar KACE (TODO en uno)

KACE simplifica TODO el proceso:

* 🔧 Compila el firmware
* ⚙️ Genera el `printer.cfg`
* 🚀 Deja Klipper listo para usar

---

## ⚡ Instalación rápida (vía SSH)

En MobaXterm, copiar y pegar:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

---

## 🚀 Ejecutar KACE

```bash
git clone https://github.com/3D-uy/KACE.git kace
cd kace
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

---

## 🧠 Dentro de KACE

1. Selecciona tu placa (ej: SKR 1.4 / Turbo)
2. KACE se encarga del resto automáticamente

✔ Firmware listo para flashear
✔ `printer.cfg` generado
✔ Configuración optimizada

---

# 💾 PARTE 6 — Flashear la SKR

1. Ir a:

```
/home/pi/klipper/out/
```

2. Descargar:

```
klipper.bin
```

3. Renombrar a:

```
firmware.bin
```

4. Copiar a la SD de la SKR
5. Insertar en la impresora
6. Encender

## ✔ Si cambia a FIRMWARE.CUR → perfecto

---

# 🧠 PARTE 7 — Aplicar configuración

1. Descargar el `printer.cfg` generado por KACE
2. Subirlo a Mainsail (**Machine**)
3. Reemplazar si es necesario

---

# 🔄 PARTE 8 — Reiniciar sistema

```bash
sudo reboot
```

Reiniciar también la impresora.

---

