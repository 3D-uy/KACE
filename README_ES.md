<p align="center">
  <img src="assets/kace_banner2.png" width="1000">
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
- Desplegarlo directamente en tu host de impresora

---

## ⚡ Inicio Rápido (vía SSH)

Para descargar este script, es necesario tener **git** instalado.  
Si no lo tienes instalado o no estás seguro, ejecuta el siguiente comando:

```bash
sudo apt-get update && sudo apt-get install git -y
```

Ejecuta KACE directamente en tu host Klipper con estos comandos optimizados:

## # 1. 
  - Clonar el repositorio
  - Instalar dependencias (con bypass para SO modernos)
  - Iniciar el Ecosistema
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt
clear
python3 KACE.py
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

*Desarrollado para la Comunidad de Klipper.*
