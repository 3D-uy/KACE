<p align="center">
  <img src="../../assets/kace_banner.png" width="1000">
</p>

# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automatización-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[English (EN)](README.md) | [Português (BR)](README_BR.md)


### KACE genera automáticamente un printer.cfg de Klipper funcional
### detectando tu hardware y guiándote a través de la configuración.


## 🟢 ¿Por qué KACE?

Configurar Klipper puede ser complejo para los nuevos usuarios.

KACE simplifica el proceso al:
- Detectar tu MCU automáticamente
- Sugerir placas compatibles
- Guiarte a través de la configuración
- Generar un printer.cfg listo para usar

---

## ⚠️ Aviso Legal

KACE se proporciona como una herramienta de código abierto destinada a simplificar la creación de una configuración de Klipper.

Al usar este software, reconoces que lo haces **bajo tu propio riesgo**.  
El autor no asume **ninguna responsabilidad por posibles daños al hardware, configuraciones incorrectas o comportamientos inesperados** resultantes de la configuración generada.

Siempre revisa y verifica el `printer.cfg` generado antes de usar tu impresora.


## 📋 Requisitos Previos

Antes de usar **KACE**, asegúrate de que los siguientes pasos ya estén completados:

✔ La tarjeta SD de la Raspberry Pi ha sido flasheada usando **Raspberry Pi Imager** con **MainsailOS**

✔ Klipper, Moonraker y Mainsail están corriendo en la Raspberry Pi

✔ **KIAUH** ha sido instalado en la Raspberry Pi

✔ El firmware de la impresora ha sido compilado usando KIAUH  

✔ El firmware compilado ha sido flasheado a la placa de control de tu impresora

Una vez completados estos pasos, puedes usar **KACE** para generar un `printer.cfg` limpio y estructurado.

---

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

---

## 🛠️ Características Principales

| Característica | Descripción |
| :--- | :--- |
| **GitHub Scraper** | Obtiene asignaciones de pines en tiempo real directamente de la fuente oficial de Klipper. |
| **Asistente Inteligente** | Autodetecta IDs seriales de MCU y te guía a través de la selección de hardware. |
| **Desplegador SSH** | Envía automáticamente tu configuración generada al host a través de SSH seguro. |
| **Motor Jinja2** | Genera configuraciones limpias, modulares y bien comentadas. |

---

## 🙏 Agradecimientos

KACE no existiría sin el increíble trabajo de las comunidades de **Klipper** y **KIAUH**.

Su dedicación, innovación y espíritu de código abierto han hecho que la impresión 3D avanzada sea accesible para miles de usuarios en todo el mundo.

KACE fue creado para contribuir de vuelta a este ecosistema haciendo la configuración inicial más fácil y accesible para los nuevos usuarios de Klipper.

*Desarrollado para la Comunidad de Klipper.*
