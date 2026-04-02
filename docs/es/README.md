<p align="center">
  <img src="../assets/kace_banner.png" width="1000">
</p>

<h1 align="center">🚀 KACE — Klipper Automated Configuration Ecosystem</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-beta-orange?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/version-v0.1.0--beta-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi-green?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/github/license/3D-uy/KACE?style=flat-square" alt="License">
</p>

<p align="center">

🌐 **Idioma**  
🇺🇸 <a href="../../README.md">English</a> | 🇪🇸 Español | 🇧🇷 <a href="../pt/README.md">Português</a>

</p>

---

## ⚡ Instala Klipper sin dolores de cabeza

KACE automatiza todo el proceso de configuración de **Klipper**, desde la detección de hardware hasta la generación de firmware y configuración lista para usar.

👉 Menos errores  
👉 Menos tiempo  
👉 Más impresión

---

## 🧠 ¿Qué es KACE realmente?

KACE ya no es solo un generador de `printer.cfg`.

Es un **motor inteligente de configuración y firmware** que:

- 🔍 Detecta automáticamente tu hardware (MCU)
- 🧠 Interpreta tu sistema sin configuraciones manuales
- ⚙️ Genera `printer.cfg` listo para usar
- 🔥 Compila automáticamente el firmware (`klipper.bin`)
- 🧭 Te guía solo cuando es necesario

---

## 🎯 ¿Por qué KACE?

Configurar Klipper manualmente implica:

- errores en firmware  
- configs incompatibles  
- pasos complejos y confusos  

**KACE elimina todo eso:**

- ✅ Automatiza decisiones técnicas complejas  
- ✅ Reduce errores críticos  
- ✅ Funciona con configuraciones reales de Klipper  
- ✅ Minimiza interacción del usuario  

---

## ⚠️ Aviso

KACE es una herramienta open-source diseñada para simplificar la configuración de Klipper.

El uso del software es **bajo tu propia responsabilidad**.

👉 Siempre revisa el `printer.cfg` generado  
👉 Verifica el firmware antes de flashear  

El autor no se responsabiliza por daños de hardware o configuraciones incorrectas.

---

## 📋 Requisitos (actualizado)

Antes de usar KACE:

✔ Raspberry Pi con **Mainsail OS** (recomendado)  
✔ Klipper instalado (KACE puede integrarse en este paso en el futuro)  
✔ Conexión SSH a tu Raspberry  

❌ Ya NO necesitas:
  
- Compilar firmware manualmente  
- Crear el archivo printer.cfg

---

## 🟡 Estado del Proyecto — Beta 1

> KACE está actualmente en **beta activo**. Las funciones principales están funcionando, pero pueden aparecer problemas menores.

| Funcionalidad | Estado |
|---|---|
| Auto-detección de MCU | ✅ Funcionando |
| GitHub Scraper | ✅ Funcionando |
| Generación de `printer.cfg` | ✅ Funcionando |
| Compilación de Firmware | ✅ Funcionando |
| Deploy via SSH | ✅ Funcionando |
| Instalación en una línea | ✅ Funcionando |
| Interfaz GUI / Web | 🚧 Planificado |

---

## ⚡ Instalación en una línea

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
```

> Esto instalará todas las dependencias, clonará el repositorio y configurará el comando global `kace` automáticamente.

---

## ⚡ Inicio rápido

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y

git clone https://github.com/3D-uy/KACE.git ~/kace
cd ~/kace
pip3 install -r requirements.txt --break-system-packages
kace
```

O con el instalador:

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh) && kace
```

---

## 🧭 Flujo de uso

KACE automatiza todo el proceso:

1. 🔍 Detecta tu MCU automáticamente
2. 📦 Busca configuraciones oficiales en Klipper
3. 🧠 Sugiere opciones compatibles
4. ⚙️ Genera `printer.cfg` optimizado
5. 🔥 Compila firmware automáticamente
6. 📁 Guarda todo en `~/kace/`

---

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
sudo systemctl restart klipper moonraker
```

---

## 🛠️ Características principales

| Característica               | Descripción                            |
| ---------------------------- | -------------------------------------- |
| 🔍 **Auto-detección de MCU** | Identifica tu hardware automáticamente |
| 🧠 **Motor inteligente**     | Deriva configuración sin templates     |
| ⚙️ **Config Generator**      | Genera `printer.cfg` limpio            |
| 🔥 **Firmware Builder**      | Compila firmware automáticamente       |
| 🧪 **Validación previa**     | Evita errores antes de compilar        |
| 🌐 **GitHub Scraper**        | Usa configs oficiales de Klipper       |
| 💻 **CLI interactiva**       | UX simple y guiada                     |

---

## 🧠 Cómo funciona (concepto)

KACE utiliza un sistema híbrido:

* Derivación automática basada en MCU
* Validación antes de compilar
* Interacción solo cuando es necesario

👉 Sin templates
👉 Sin configuraciones estáticas
👉 Sin dependencia de herramientas externas

---

## 🎬 Guías completas

👉 Documentación completa:

* 🇺🇸 English: `../en/README.md`
* 🇪🇸 Español: *(esta página)*
* 🇧🇷 Português: `../pt/README.md`

👉 Instalación Pi Imager:

* 🇺🇸 English: `../en/pi_imager.md`
* 🇪🇸 Español: *(esta página)*
* 🇧🇷 Português: `../pt/pi_imager.md`

👉 Instalación Klipper Completa:


* 🇺🇸 English: `../en/klipper_install.md`
* 🇪🇸 Español: *(esta página)*
* 🇧🇷 Português: `../pt/klipper_install.md`

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

