# 🚀 KLIPPER instalación fácil

![Firmware](https://img.shields.io/badge/Firmware-Klipper-orange)
![Board](https://img.shields.io/badge/Board-SKR%201.4%20%2F%201.4%20Turbo-blue)
![Raspberry](https://img.shields.io/badge/Raspberry-Pi%203B-red)
![Interface](https://img.shields.io/badge/UI-Mainsail-purple)
![Guide](https://img.shields.io/badge/Guía-Instalación%20simple-success)

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

# 🧰 PARTE 5 — Instalación de KIAUH

## Instalación de KIAUH
Sitio oficial: ([https://github.com/dw-0/kiauh](https://github.com/dw-0/kiauh))

## Paso 1
Para descargar este script es necesario tener **git** instalado.  
Si no lo tienes instalado o no estás seguro, ejecuta el siguiente comando:

```
sudo apt-get update && sudo apt-get install git -y
```

## Paso 2
Una vez que **git** esté instalado, usa el siguiente comando para descargar KIAUH en tu directorio *home*:

```
cd ~ && git clone https://github.com/dw-0/kiauh.git
```

## Paso 3
Finalmente, inicia KIAUH ejecutando el siguiente comando:

```
./kiauh/kiauh.sh
```

---

# ⚙️ PARTE 6 — Compilar firmware usando KIAUH

En el menú seleccionar:

  ## 4 → Advanced
  ## 1 → Build

Seleccionar la opción para configurar:

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

### Pulsa **Q** para salir y te preguntará si quieres guardar.
### Presiona **Y** para aceptar y continuar con la creación del firmware.
#----------------------------------------------------------#

El firmware se generará en:
/home/pi/klipper/out/klipper.bin

---

# 💾 PARTE 7 — Flashear la SKR En MobaXterm:

1. Ir a:
```
/home/pi/klipper/out/
```
2. Descargar klipper.bin
3. Renombrarlo a:

  ## firmware.bin (para placas SKR)

4. Copiar el archivo firmware.bin a la SD de la SKR.
5. Insertar SD en la SKR.
6. Encender impresora.

## Si el archivo en la SD cambia a FIRMWARE.CUR → se flasheó correctamente.

---

# 🧠 PARTE 8 — Instalar KACE 
(https://github.com/3D-uy/kace)

### Conectar USB entre Raspberry y SKR.
### Encender impresora.

En terminal:
## ⚡ Inicio Rápido (vía SSH)

Para descargar este script, es necesario tener **git** instalado.  
Si no lo tienes instalado o no estás seguro, ejecuta el siguiente comando:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

Ejecuta KACE directamente en tu host Klipper con estos comandos optimizados:

## # 1. 
  - Clonar el repositorio
  - Instalar dependencias (con bypass para SO modernos)
  - Iniciar el Ecosistema
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

## # 2.

  -Descarga el archivo printer.cfg recién creado y súbelo a Klipper.

## # 3. 

  -Reinicia el sistema desde SSH
  
```
sudo reboot
```
## Reinicia la impresora y la raspberry.
### Ya Mainsailos deberia de estar corriendo en tu raspberry y el archivo 
### printer.cfg deberias encontrarlo en el apartado de MACHINE.

# 🎉 HAPPY PRINTING!

Tu impresora ahora debería estar corriendo Klipper y estás listo para hacer los ajustes necesarios y comenzar con las macros.
