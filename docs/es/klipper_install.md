# 🚀 KLIPPER instalación fácil

![Firmware](https://img.shields.io/badge/Firmware-Klipper-orange)
![Board](https://img.shields.io/badge/Board-SKR%201.4%20%2F%201.4%20Turbo-blue)
![Raspberry](https://img.shields.io/badge/Raspberry-Pi%203B-red)
![Interface](https://img.shields.io/badge/UI-Mainsail-purple)
![Guide](https://img.shields.io/badge/Guía-Instalación%20simple-success)

<p align="center">

🌐 **Idioma**  
🇺🇸 <a href="../en/klipper_install.md">English</a> | 🇪🇸 Español | 🇧🇷 <a href="../pt/klipper_install.md">Português</a>

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

Guia para instalar **Raspberry Pi Imager** <a href="pi_imager.md">pi_imager</a>

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

# ⚡ PARTE — Instalar y usar KACE (TODO en uno)

KACE simplifica TODO el proceso:

* 🔧 Compila el firmware
* ⚙️ Genera el `printer.cfg`
* 🚀 Deja Klipper listo para usar

---


## ⚡ Instalación en una línea

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
```

> Esto instalará todas las dependencias, clonará el repositorio y configurará el comando global `kace` automáticamente.

## 📦 Resultado final

Después de ejecutar KACE tendrás:

```
~/kace/
├── printer.cfg
├── klipper.bin / klipper.uf2 / klipper.hex
```

---

## 🚀 Siguientes pasos

1. Flashear firmware en tu placa (SD / USB)
2. Subir `printer.cfg` a Klipper
3. Reiniciar servicios:

```bash
sudo reboot
```

---

### 🎉 LISTO PARA EMPEZAR

Ya tienes tu firmware compilado y tu archivo `printer.cfg` generado automáticamente.

Ahora solo queda ajustarlo a tus necesidades, calibrar tu impresora y empezar a sacarle todo el potencial a Klipper.

🚀 ¡Disfruta el proceso y HAPPY PRINTING!

---

## 🙌 Contribuir y feedback

KACE evoluciona con la comunidad:

* 🐛 Reportar bugs
* 💡 Sugerir mejoras
* 🤝 Contribuir código

👉 Todo aporte suma.

---

## 🙏 Agradecimientos

Este proyecto se apoya en el trabajo increíble de la comunidad de **Klipper**.

KACE busca hacer ese ecosistema más accesible para todos.

---

<p align="center">

⭐ Si te gusta este proyecto, dale una estrella
🚀 Hecho para simplificar Klipper

</p>


---

