<p align="center">
  <img src="docs/assets/kace_banner.png" width="1000">
</p>

# 🚀 KACE — Klipper Automated Configuration Ecosystem

<p align="center">

🌐 **Idioma**  
🇺🇸 <a href="README.md">English</a> | 🇪🇸 Español | 🇧🇷 <a href="docs/pt/README.md">Português</a>

</p>

---

### ⚡ Instala Klipper de forma fácil — copiar, pegar y listo.

KACE genera automáticamente un **`printer.cfg` funcional para Klipper**, detectando tu hardware y guiándote a través de un proceso de configuración inteligente.

---

## 🎯 ¿Por qué KACE?

Configurar Klipper puede ser complejo y llevar mucho tiempo, especialmente para usuarios nuevos.

**KACE simplifica todo:**

- 🔍 Detecta automáticamente tu MCU  
- 🧠 Sugiere placas compatibles  
- 🧭 Te guía paso a paso  
- ⚙️ Genera un `printer.cfg` listo para usar  

---

## ⚠️ Aviso

KACE se proporciona como una herramienta de código abierto destinada a simplificar la creación de configuraciones para Klipper.

Al utilizar este software, reconoces que lo haces **bajo tu propia responsabilidad**.  
El autor no asume **ninguna responsabilidad por posibles daños de hardware, configuraciones incorrectas o comportamientos inesperados** derivados del uso de la configuración generada.

👉 Siempre revisa y verifica el archivo `printer.cfg` antes de usar tu impresora.

---

## 📋 Requisitos previos

Antes de usar **KACE**, asegúrate de haber completado lo siguiente:

✔ Tarjeta SD de Raspberry Pi grabada con **Raspberry Pi Imager** usando **Mainsail OS**  
✔ Klipper, Moonraker y Mainsail en funcionamiento  
✔ **KIAUH** instalado en la Raspberry Pi  
✔ Firmware compilado usando KIAUH  
✔ Firmware cargado en la placa controladora de la impresora  

Una vez completado, KACE se encarga del resto.

---

## ⚡ Inicio rápido (vía SSH)

Asegúrate de tener `git` instalado:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
````

---

### 🚀 Ejecutar KACE

```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

---

### 📥 Siguientes pasos

1. Descargar el archivo `printer.cfg` generado
2. Subirlo a tu interfaz de Klipper
3. Reiniciar los servicios:

```bash
sudo systemctl restart klipper moonraker
```

---

## 🛠️ Características principales

| Característica               | Descripción                                          |
| :--------------------------- | :--------------------------------------------------- |
| 🔎 **GitHub Scraper**        | Obtiene pinouts en tiempo real desde Klipper         |
| 🧠 **Asistente inteligente** | Detecta el MCU y guía la selección de hardware       |
| 🔐 **Despliegue por SSH**    | Envía automáticamente la configuración al host       |
| ⚙️ **Motor Jinja2**          | Genera configuraciones limpias, modulares y legibles |

---

## 🎬 Guía completa de instalación

👉 Guías paso a paso:

* 🇺🇸 English: `../../README.md`
* 🇪🇸 Español: *(esta página)*
* 🇧🇷 Português: `../pt/README.md`

---

## 🙌 Contribuir y feedback

KACE está en constante evolución y tu feedback es clave.

* 🐛 Reportar errores
* 💡 Sugerir mejoras
* 🤝 Aportar ideas

👉 Cada aporte ayuda a mejorar el proyecto.

---

## 🙏 Agradecimientos

KACE no existiría sin el increíble trabajo de las comunidades de **Klipper** y **KIAUH**.

Su dedicación, innovación y espíritu open-source han hecho que la impresión 3D avanzada sea accesible para miles de usuarios en todo el mundo.

KACE nace como una forma de aportar a este ecosistema, haciendo la configuración inicial más simple y accesible.

---

<p align="center">

⭐ Si te gusta este proyecto, considera darle una estrella
🚀 Hecho para la comunidad de Klipper

</p>


