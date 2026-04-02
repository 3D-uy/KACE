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
🌐 <strong>Idioma</strong><br>
🇺🇸 <a href="../../README.md">English</a> | 🇪🇸 Español | 🇧🇷 <a href="../pt/README.md">Português</a>
</p>

> [!WARNING]
> **KACE está actualmente en Beta.** Las funciones principales están funcionando, pero pueden aparecer bugs o problemas menores.
> Siempre revisa los archivos generados antes de usarlos. Reporta problemas usando el template [Bug Report](../../.github/ISSUE_TEMPLATE/bug_report.md).

---

## ⚡ Instala Klipper sin dolores de cabeza

KACE automatiza todo el proceso de configuración de **Klipper**, desde la detección de hardware hasta la generación de firmware y configuración lista para usar.

👉 Menos errores  
👉 Menos tiempo  
👉 Más impresión

---

## 🧠 ¿Qué es KACE realmente?

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

## 📋 Requisitos

Antes de usar KACE:

✔ Raspberry Pi Imager instalado en la SD: incluye **Klipper**, **Mainsail OS**, **Moonraker** (recomendado)  
✔ Acceso SSH a tu Raspberry Pi (Mobaxterm)  

❌ Ya NO necesitas:

- Compilar firmware manualmente  
- Crear el archivo printer.cfg

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
sudo reboot
```

---

## 🛠️ Características principales

| Característica | Descripción |
| --- | --- |
| 🔍 **Auto-detección de MCU** | Identifica tu hardware automáticamente |
| 🧠 **Motor inteligente** | Deriva configuración sin templates |
| ⚙️ **Config Generator** | Genera `printer.cfg` limpio |
| 🔥 **Firmware Builder** | Compila firmware automáticamente |
| 🧪 **Validación previa** | Evita errores antes de compilar |
| 🌐 **GitHub Scraper** | Usa configs oficiales de Klipper |
| 💻 **CLI interactiva** | UX simple y guiada |

---

## 🧠 Cómo funciona (concepto)

KACE utiliza un sistema híbrido:

- Derivación automática basada en MCU
- Validación antes de compilar
- Interacción solo cuando es necesario

👉 Sin templates  
👉 Sin configuraciones estáticas  
👉 Sin dependencia de herramientas externas

---

## ⚠️ Aviso

KACE es una herramienta open-source diseñada para simplificar la configuración de Klipper.

El uso del software es **bajo tu propia responsabilidad**.  
El autor no se responsabiliza por **daños de hardware, configuraciones incorrectas o comportamientos inesperados** resultantes de la configuración generada.

👉 Siempre revisa el `printer.cfg` generado antes de usar tu impresora.  
👉 Verifica el firmware antes de flashear.

---

## 🗑️ Desinstalar

Para eliminar KACE de tu sistema:

```bash
# Eliminar el symlink del comando global
sudo rm -f /usr/local/bin/kace

# O si se instaló sin sudo (fallback)
rm -f ~/.local/bin/kace

# Eliminar el directorio de KACE
rm -rf ~/kace
```

---

## 🎬 Guías completas

👉 Documentación completa:

* 🇺🇸 English: `../../README.md`
* 🇪🇸 Español: *(esta página)*
* 🇧🇷 Português: `../pt/README.md`

👉 Instalación Pi Imager:
* 🇺🇸 English: `../../docs/en/pi_imager_install.md`
* 🇪🇸 Español: `pi_imager.md`
* 🇧🇷 Português: `../pt/pi_imager.md`

👉 Instalación Klipper Completa:
* 🇺🇸 English: `../../docs/en/Klipper_install.md`
* 🇪🇸 Español: `klipper_install.md`
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
