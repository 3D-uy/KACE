# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automatización-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[English (EN)](README.md) | [Português (BR)](README_BR.md)

KACE es una herramienta de automatización de alto rendimiento diseñada para eliminar la complejidad manual de crear un `printer.cfg`. Cierra la brecha entre el hardware puro y una instalación de Klipper perfectamente ajustada.

---

## ⚡ Inicio Rápido (vía SSH)

Para descargar este script es necesario tener **git** instalado.  
Si no lo tienes instalado o no estás seguro, ejecuta el siguiente comando:

```
sudo apt-get update && sudo apt-get install git -y
```

Ejecuta KACE directamente en tu host Klipper con estos comandos optimizados:

# 1. Clonar el repositorio
```
git clone https://github.com/3D-uy/KACE.git
cd KACE
```
# 2. Instalar dependencias (con bypass para SO modernos)
```
pip3 install -r requirements.txt --break-system-packages
```
# 3. Iniciar el Ecosistema
```
python3 main.py
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

## 📦 Instalación Manual

1. **Descargar**: Haz clic en **"Download Project (.zip)"** en el portal de KACE.
2. **Subir**: Arrastra la carpeta `kace` a tu Pi a través de MobaXterm SFTP.
3. **Ejecutar**: Ejecuta `python3 main.py` en la terminal.

---

*Desarrollado para la Comunidad de Klipper.*
