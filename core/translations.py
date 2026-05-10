# core/translations.py

# ── i18n: UI String Layer ──────────────────────────────────────
# Language state — set once after the user's language choice, then
# read by all modules via get_lang() so callers never thread lang
# through every function signature.

_current_lang = "English"

_SUPPORTED_LANGS = ("English", "Español", "Português")


def set_lang(lang: str) -> None:
    """Set the active UI language for the current session."""
    global _current_lang
    if lang in _SUPPORTED_LANGS:
        _current_lang = lang


def get_lang() -> str:
    """Return the active UI language."""
    return _current_lang


# All user-facing UI strings keyed by a short dot-separated ID.
# Each entry maps language name → display string.
# Strings may contain {placeholders} for str.format(**kwargs).
# Detection paths listed here use standard Klipper defaults and
# are kept in one place to make future configurability easy.
UI_STRINGS: dict = {
    # ── Wizard prompts ─────────────────────────────────────────
    "wizard.select_language": {
        "English":   "Select language for comments / Seleccione el idioma / Selecione o idioma:",
        "Español":   "Seleccione el idioma para comentarios:",
        "Português": "Selecione o idioma para comentários:",
    },
    "wizard.select_printer_model": {
        "English":   "Select your Printer Model (type to search) [Ctrl+C to go back]:",
        "Español":   "Seleccione el modelo de impresora (escriba para buscar) [Ctrl+C para volver]:",
        "Português": "Selecione o modelo de impressora (digite para buscar) [Ctrl+C para voltar]:",
    },
    "wizard.select_board": {
        "English":   "Select your Board:",
        "Español":   "Seleccione su placa:",
        "Português": "Selecione sua placa:",
    },
    "wizard.select_board_suggested": {
        "English":   "Suggested boards based on your MCU:",
        "Español":   "Placas sugeridas según su MCU:",
        "Português": "Placas sugeridas com base no seu MCU:",
    },
    "wizard.select_board_manual": {
        "English":   "Select your board manually (type to search) [Ctrl+C to go back]:",
        "Español":   "Seleccione su placa manualmente (escriba para buscar) [Ctrl+C para volver]:",
        "Português": "Selecione sua placa manualmente (digite para buscar) [Ctrl+C para voltar]:",
    },
    "wizard.select_kinematics": {
        "English":   "Select Kinematics:",
        "Español":   "Seleccione la Cinemática:",
        "Português": "Selecione a Cinemática:",
    },
    "wizard.x_volume": {
        "English":   "Enter X build volume (mm) [Ctrl+C to go back]:",
        "Español":   "Ingrese el volumen de construcción X (mm) [Ctrl+C para volver]:",
        "Português": "Digite o volume de impressão X (mm) [Ctrl+C para voltar]:",
    },
    "wizard.y_volume": {
        "English":   "Enter Y build volume (mm) [Ctrl+C to go back]:",
        "Español":   "Ingrese el volumen de construcción Y (mm) [Ctrl+C para volver]:",
        "Português": "Digite o volume de impressão Y (mm) [Ctrl+C para voltar]:",
    },
    "wizard.z_volume": {
        "English":   "Enter Z build volume (mm) [Ctrl+C to go back]:",
        "Español":   "Ingrese el volumen de construcción Z (mm) [Ctrl+C para volver]:",
        "Português": "Digite o volume de impressão Z (mm) [Ctrl+C para voltar]:",
    },
    "wizard.select_probe": {
        "English":   "Select Probe Type:",
        "Español":   "Seleccione el Tipo de Sensor:",
        "Português": "Selecione o Tipo de Sensor:",
    },
    "wizard.select_hotend_therm": {
        "English":   "Select Hotend Thermistor:",
        "Español":   "Seleccione el Termistor del Hotend:",
        "Português": "Selecione o Termistor do Hotend:",
    },
    "wizard.custom_hotend_therm": {
        "English":   "Enter custom hotend thermistor name:",
        "Español":   "Ingrese el nombre personalizado del termistor del hotend:",
        "Português": "Digite o nome personalizado do termistor do hotend:",
    },
    "wizard.select_bed_therm": {
        "English":   "Select Bed Thermistor:",
        "Español":   "Seleccione el Termistor de la Cama:",
        "Português": "Selecione o Termistor da Mesa:",
    },
    "wizard.custom_bed_therm": {
        "English":   "Enter custom bed thermistor name:",
        "Español":   "Ingrese el nombre personalizado del termistor de la cama:",
        "Português": "Digite o nome personalizado do termistor da mesa:",
    },
    "wizard.select_driver": {
        "English":   "Select Stepper Driver Type:",
        "Español":   "Seleccione el Tipo de Driver de Motores:",
        "Português": "Selecione o Tipo de Driver de Motores:",
    },
    "wizard.select_driver_mode": {
        "English":   "Select {driver} Communication Mode:",
        "Español":   "Seleccione el Modo de Comunicación del {driver}:",
        "Português": "Selecione o Modo de Comunicação do {driver}:",
    },
    "wizard.z_motors": {
        "English":   "How many Z motor drivers are you using?",
        "Español":   "¿Cuántos drivers para motores Z está utilizando?",
        "Português": "Quantos drivers para motores Z você está usando?",
    },
    "wizard.select_web_ui": {
        "English":   "Select your Web Interface (for includes):",
        "Español":   "Seleccione su Interfaz Web (para includes):",
        "Português": "Selecione sua Interface Web (para includes):",
    },
    "wizard.select_driver_z": {
        "English":   "Select driver for {motor}:",
        "Español":   "Seleccione el driver para {motor}:",
        "Português": "Selecione o driver para {motor}:",
    },
    "wizard.mapping_pins": {
        "English":   ">>> Mapping pins for [ {motor} ] ...",
        "Español":   ">>> Asignando pines para [ {motor} ] ...",
        "Português": ">>> Mapeando pinos para [ {motor} ] ...",
    },
    "wizard.no_drivers_warning": {
        "English":   "Warning: Your board does not have enough available stepper drivers in its config for this Z motor.",
        "Español":   "Advertencia: Su placa no tiene suficientes drivers disponibles para este motor Z.",
        "Português": "Aviso: Sua placa não tem drivers disponíveis suficientes para este motor Z.",
    },
    "wizard.custom_step_pin": {
        "English":   "Enter step_pin (e.g. PC4):",
        "Español":   "Ingrese step_pin (ej. PC4):",
        "Português": "Digite step_pin (ex. PC4):",
    },
    "wizard.custom_dir_pin": {
        "English":   "Enter dir_pin (e.g. PA6):",
        "Español":   "Ingrese dir_pin (ej. PA6):",
        "Português": "Digite dir_pin (ex. PA6):",
    },
    "wizard.custom_en_pin": {
        "English":   "Enter enable_pin (e.g. !PC5):",
        "Español":   "Ingrese enable_pin (ej. !PC5):",
        "Português": "Digite enable_pin (ex. !PC5):",
    },
    "wizard.custom_uart_pin": {
        "English":   "Enter {mode}_pin for {motor}:",
        "Español":   "Ingrese {mode}_pin para {motor}:",
        "Português": "Digite {mode}_pin para {motor}:",
    },
    # ── Common choice labels ────────────────────────────────────
    "choice.back": {
        "English":   "Back",
        "Español":   "Volver",
        "Português": "Voltar",
    },
    "choice.quit": {
        "English":   "Quit",
        "Español":   "Salir",
        "Português": "Sair",
    },
    "choice.search_manually": {
        "English":   "Search manually...",
        "Español":   "Buscar manualmente...",
        "Português": "Buscar manualmente...",
    },
    "choice.custom_scratch": {
        "English":   "Custom / Scratch Build",
        "Español":   "Construcción Personalizada / Desde Cero",
        "Português": "Construção Personalizada / Do Zero",
    },
    "choice.stock_board": {
        "English":   "Stock Board (from printer profile)",
        "Español":   "Placa de Fábrica (del perfil de la impresora)",
        "Português": "Placa de Fábrica (do perfil da impressora)",
    },
    "choice.other_manual": {
        "English":   "Other (Manual Entry)",
        "Español":   "Otro (Ingreso Manual)",
        "Português": "Outro (Entrada Manual)",
    },
    "choice.custom_pins": {
        "English":   "Custom pin assignment",
        "Español":   "Asignación de pines personalizada",
        "Português": "Atribuição de pinos personalizada",
    },
    "choice.quit_setup": {
        "English":   "Quit setup",
        "Español":   "Salir de la configuración",
        "Português": "Sair da configuração",
    },
    # ── Dashboard strings ───────────────────────────────────────
    "dashboard.status_title": {
        "English":   "System Status",
        "Español":   "Estado del Sistema",
        "Português": "Status do Sistema",
    },
    "dashboard.installed": {
        "English":   "Installed",
        "Español":   "Instalado",
        "Português": "Instalado",
    },
    "dashboard.not_found": {
        "English":   "Not found",
        "Español":   "No encontrado",
        "Português": "Não encontrado",
    },
    "dashboard.found": {
        "English":   "Found",
        "Español":   "Encontrado",
        "Português": "Encontrado",
    },
    "dashboard.detected": {
        "English":   "detected",
        "Español":   "detectado",
        "Português": "detectado",
    },
    "dashboard.no_mcu": {
        "English":   "None detected",
        "Español":   "Ninguno detectado",
        "Português": "Nenhum detectado",
    },
    "dashboard.action_prompt": {
        "English":   "What would you like to do?",
        "Español":   "¿Qué desea hacer?",
        "Português": "O que você gostaria de fazer?",
    },
    "dashboard.action_generate": {
        "English":   "Generate new config",
        "Español":   "Generar nueva configuración",
        "Português": "Gerar nova configuração",
    },
    "dashboard.action_reconfig": {
        "English":   "Reconfigure existing printer",
        "Español":   "Reconfigurar impresora existente",
        "Português": "Reconfigurar impressora existente",
    },
    "dashboard.action_manage": {
        "English":   "View component status",
        "Español":   "Ver estado de componentes",
        "Português": "Ver status dos componentes",
    },
    "dashboard.action_quit": {
        "English":   "Quit",
        "Español":   "Salir",
        "Português": "Sair",
    },
    "dashboard.suggestions_header": {
        "English":   "Suggestions",
        "Español":   "Sugerencias",
        "Português": "Sugestões",
    },
    "dashboard.suggest_no_klipper": {
        "English":   "Klipper not found — install it via KACE or install.sh",
        "Español":   "Klipper no encontrado — instálelo con KACE o install.sh",
        "Português": "Klipper não encontrado — instale-o via KACE ou install.sh",
    },
    "dashboard.suggest_no_moonraker": {
        "English":   "Moonraker not found — instálelo para habilitar el control web",
        "Español":   "Moonraker no encontrado — instálelo para habilitar el control web",
        "Português": "Moonraker não encontrado — instale-o para habilitar o controle web",
    },
    "dashboard.suggest_no_webui": {
        "English":   "No web UI detected — consider installing Mainsail or Fluidd",
        "Español":   "No se detectó interfaz web — considere instalar Mainsail o Fluidd",
        "Português": "Nenhuma interface web detectada — considere instalar Mainsail ou Fluidd",
    },
    "dashboard.suggest_no_cfg": {
        "English":   "No printer.cfg found — run 'Generate new config' to create one",
        "Español":   "No se encontró printer.cfg — ejecute 'Generar nueva configuración'",
        "Português": "Nenhum printer.cfg encontrado — execute 'Gerar nova configuração'",
    },
    "dashboard.manage_header": {
        "English":   "Component Status",
        "Español":   "Estado de Componentes",
        "Português": "Status dos Componentes",
    },
    "dashboard.press_enter": {
        "English":   "Press Enter to return to the menu...",
        "Español":   "Presione Enter para volver al menú...",
        "Português": "Pressione Enter para voltar ao menu...",
    },
    "dashboard.crowsnest": {
        "English":   "Crowsnest",
        "Español":   "Crowsnest",
        "Português": "Crowsnest",
    },
    # ── kace.py messages ────────────────────────────────────────
    "kace.cancelled": {
        "English":   "Setup cancelled by user.",
        "Español":   "Configuración cancelada por el usuario.",
        "Português": "Configuração cancelada pelo usuário.",
    },
    "kace.missing_dep": {
        "English":   "Missing dependency: {error}",
        "Español":   "Dependencia faltante: {error}",
        "Português": "Dependência ausente: {error}",
    },
    "kace.missing_dep_hint": {
        "English":   "Run: pip3 install -r requirements.txt --break-system-packages",
        "Español":   "Ejecute: pip3 install -r requirements.txt --break-system-packages",
        "Português": "Execute: pip3 install -r requirements.txt --break-system-packages",
    },
    "kace.skip_firmware": {
        "English":   "Skipping firmware compilation (no MCU designated).",
        "Español":   "Omitiendo compilación de firmware (sin MCU designado).",
        "Português": "Ignorando compilação de firmware (sem MCU designado).",
    },
    "kace.compile_prompt": {
        "English":   "Do you want to automatically compile Klipper firmware for your {mcu}?",
        "Español":   "¿Desea compilar automáticamente el firmware de Klipper para su {mcu}?",
        "Português": "Deseja compilar automaticamente o firmware do Klipper para seu {mcu}?",
    },
    "kace.compiling": {
        "English":   "Rebuilding Klipper firmware for your controller...",
        "Español":   "Recompilando firmware de Klipper para su controlador...",
        "Português": "Recompilando firmware do Klipper para seu controlador...",
    },
    "kace.firmware_success": {
        "English":   "Firmware built locally at {path}",
        "Español":   "Firmware compilado localmente en {path}",
        "Português": "Firmware compilado localmente em {path}",
    },
    "kace.firmware_error": {
        "English":   "Firmware build failed: {message}",
        "Español":   "Error al compilar firmware: {message}",
        "Português": "Falha na compilação do firmware: {message}",
    },
    "kace.deploy_firmware_prompt": {
        "English":   "Select Deployment Method for Firmware (klipper.bin/.uf2/.hex):",
        "Español":   "Seleccione el Método de Despliegue del Firmware (klipper.bin/.uf2/.hex):",
        "Português": "Selecione o Método de Deploy do Firmware (klipper.bin/.uf2/.hex):",
    },
    "kace.deploy_cfg_prompt": {
        "English":   "Select Deployment Method for Configuration (printer.cfg):",
        "Español":   "Seleccione el Método de Despliegue de la Configuración (printer.cfg):",
        "Português": "Selecione o Método de Deploy da Configuração (printer.cfg):",
    },
    "kace.generate_macros_prompt": {
        "English":   "Would you like to generate a starter macros configuration (macros.cfg)?",
        "Español":   "¿Desea generar una configuración de macros iniciales (macros.cfg)?",
        "Português": "Deseja gerar uma configuração de macros iniciais (macros.cfg)?",
    },
    "kace.deploy_none": {
        "English":   "None (Done)",
        "Español":   "Ninguno (Listo)",
        "Português": "Nenhum (Concluído)",
    },
    "kace.deploy_local": {
        "English":   "Local Folder (PC)",
        "Español":   "Carpeta Local (PC)",
        "Português": "Pasta Local (PC)",
    },
    "kace.deploy_usb": {
        "English":   "USB / SD Card",
        "Español":   "USB / Tarjeta SD",
        "Português": "USB / Cartão SD",
    },
    "kace.deploy_ssh": {
        "English":   "SSH (Push to host)",
        "Español":   "SSH (Enviar al host)",
        "Português": "SSH (Enviar ao host)",
    },
    "kace.deploy_avrdude": {
        "English":   "Flash via USB (avrdude)",
        "Español":   "Flashear por USB (avrdude)",
        "Português": "Gravar via USB (avrdude)",
    },
    "kace.ssh_host_prompt": {
        "English":   "Enter SSH Host (e.g. 192.168.1.100):",
        "Español":   "Ingrese el Host SSH (ej. 192.168.1.100):",
        "Português": "Digite o Host SSH (ex. 192.168.1.100):",
    },
    "kace.ssh_user_prompt": {
        "English":   "Enter SSH User (e.g. pi):",
        "Español":   "Ingrese el Usuario SSH (ej. pi):",
        "Português": "Digite o Usuário SSH (ex. pi):",
    },
    "kace.ssh_pass_prompt": {
        "English":   "Enter SSH Password:",
        "Español":   "Ingrese la Contraseña SSH:",
        "Português": "Digite a Senha SSH:",
    },
    "kace.ssh_dest_prompt": {
        "English":   "Enter Destination Path:",
        "Español":   "Ingrese la Ruta de Destino:",
        "Português": "Digite o Caminho de Destino:",
    },
    "kace.fetching_cfg": {
        "English":   "Fetching configuration for {board}...",
        "Español":   "Obteniendo configuración para {board}...",
        "Português": "Obtendo configuração para {board}...",
    },
    "kace.fetching_cfg_done": {
        "English":   "Fetching configuration for {board}... Done!",
        "Español":   "Obteniendo configuración para {board}... ¡Listo!",
        "Português": "Obtendo configuração para {board}... Concluído!",
    },
    "kace.generating_cfg": {
        "English":   "Generating printer.cfg...",
        "Español":   "Generando printer.cfg...",
        "Português": "Gerando printer.cfg...",
    },
    "kace.generating_cfg_done": {
        "English":   "Generating printer.cfg... Done!",
        "Español":   "Generando printer.cfg... ¡Listo!",
        "Português": "Gerando printer.cfg... Concluído!",
    },
    "kace.cfg_success": {
        "English":   "printer.cfg generated successfully at {path}",
        "Español":   "printer.cfg generado exitosamente en {path}",
        "Português": "printer.cfg gerado com sucesso em {path}",
    },
    "kace.abort_missing_pins": {
        "English":   "Setup aborted. Missing pins for Z motors.",
        "Español":   "Configuración abortada. Pines faltantes para motores Z.",
        "Português": "Configuração abortada. Pinos ausentes para motores Z.",
    },
    "kace.abort_valid_pins": {
        "English":   "Error: Valid pins are required to proceed. Aborting.",
        "Español":   "Error: Se requieren pines válidos para continuar. Abortando.",
        "Português": "Erro: Pinos válidos são necessários para continuar. Abortando.",
    },
    "kace.abort_no_uart": {
        "English":   "Error: {mode} pin is critically required. Aborting.",
        "Español":   "Error: El pin {mode} es imprescindible. Abortando.",
        "Português": "Erro: O pino {mode} é obligatorio. Abortando.",
    },
    "kace.abort_no_tmc_map": {
        "English":   "Error: No {mode} pin mapping found on this board for {driver}.",
        "Español":   "Error: No se encontró mapeo de pin {mode} en esta placa para {driver}.",
        "Português": "Erro: Nenhum mapeamento de pino {mode} encontrado nesta placa para {driver}.",
    },
    "kace.abort_generation": {
        "English":   "Generation aborted to prevent missing parameters.",
        "Español":   "Generación abortada para evitar parámetros faltantes.",
        "Português": "Geração abortada para evitar parâmetros ausentes.",
    },
    # ── Summary strings ─────────────────────────────────────────
    "summary.title": {
        "English":   "Setup Complete",
        "Español":   "Configuración Completada",
        "Português": "Configuração Concluída",
    },
    "summary.firmware": {
        "English":   "Firmware:",
        "Español":   "Firmware:",
        "Português": "Firmware:",
    },
    "summary.config": {
        "English":   "Config:  ",
        "Español":   "Config:  ",
        "Português": "Config:  ",
    },
    "summary.generation_details": {
        "English":   "Generation Details",
        "Español":   "Detalles de Generación",
        "Português": "Detalhes de Geração",
    },
    "summary.printer_profile": {
        "English":   "Printer Profile:",
        "Español":   "Perfil de Impresora:",
        "Português": "Perfil de Impressora:",
    },
    "summary.board_config": {
        "English":   "Board Config:",
        "Español":   "Config. de Placa:",
        "Português": "Config. de Placa:",
    },
    "summary.kinematics": {
        "English":   "Kinematics:",
        "Español":   "Cinemática:",
        "Português": "Cinemática:",
    },
    "summary.hotend_thermistor": {
        "English":   "Hotend Thermistor:",
        "Español":   "Termistor del Hotend:",
        "Português": "Termistor do Hotend:",
    },
    "summary.bed_thermistor": {
        "English":   "Bed Thermistor:",
        "Español":   "Termistor de la Cama:",
        "Português": "Termistor da Mesa:",
    },
    "summary.next_steps": {
        "English":   "Next steps:",
        "Español":   "Próximos pasos:",
        "Português": "Próximos passos:",
    },
    "summary.step1": {
        "English":   "Flash firmware to your board",
        "Español":   "Flashee el firmware en su placa",
        "Português": "Grave o firmware na sua placa",
    },
    "summary.step2": {
        "English":   "Upload printer.cfg to Klipper",
        "Español":   "Suba printer.cfg a Klipper",
        "Português": "Faça upload do printer.cfg para o Klipper",
    },
    "summary.step3": {
        "English":   "Restart Klipper",
        "Español":   "Reinicie Klipper",
        "Português": "Reinicie o Klipper",
    },
    # ── builder.py strings ──────────────────────────────────────
    "builder.summary_title": {
        "English":   "🛠  Klipper Firmware Target Summary",
        "Español":   "🛠  Resumen de Destino del Firmware de Klipper",
        "Português": "🛠  Resumo do Alvo do Firmware do Klipper",
    },
    "builder.architecture": {
        "English":   "Architecture",
        "Español":   "Arquitectura",
        "Português": "Arquitetura",
    },
    "builder.processor": {
        "English":   "Processor Model",
        "Español":   "Modelo de Procesador",
        "Português": "Modelo do Processador",
    },
    "builder.bootloader": {
        "English":   "Bootloader Offset",
        "Español":   "Offset del Bootloader",
        "Português": "Offset do Bootloader",
    },
    "builder.comm_interface": {
        "English":   "Communication Interface",
        "Español":   "Interfaz de Comunicación",
        "Português": "Interface de Comunicação",
    },
    "builder.clock": {
        "English":   "Clock Frequency",
        "Español":   "Frecuencia de Reloj",
        "Português": "Frequência de Clock",
    },
    "builder.usb_path": {
        "English":   "USB IDs / Serial Path",
        "Español":   "IDs USB / Ruta Serial",
        "Português": "IDs USB / Caminho Serial",
    },
    "builder.not_detected": {
        "English":   "Not Detected",
        "Español":   "No Detectado",
        "Português": "Não Detectado",
    },
    "builder.config_correct": {
        "English":   "Is this configuration correct? (Use arrow keys)",
        "Español":   "¿Es correcta esta configuración? (Use las flechas)",
        "Português": "Esta configuração está correta? (Use as setas)",
    },
    "builder.compile_now": {
        "English":   "🚀  Compile Firmware Now",
        "Español":   "🚀  Compilar Firmware Ahora",
        "Português": "🚀  Compilar Firmware Agora",
    },
    "builder.edit_arch": {
        "English":   "🔧  Edit Architecture",
        "Español":   "🔧  Editar Arquitectura",
        "Português": "🔧  Editar Arquitetura",
    },
    "builder.edit_proc": {
        "English":   "🔧  Edit Processor Model",
        "Español":   "🔧  Editar Modelo de Procesador",
        "Português": "🔧  Editar Modelo do Processador",
    },
    "builder.edit_boot": {
        "English":   "🔧  Edit Bootloader Offset",
        "Español":   "🔧  Editar Offset del Bootloader",
        "Português": "🔧  Editar Offset do Bootloader",
    },
    "builder.edit_comm": {
        "English":   "🔧  Edit Communication Interface",
        "Español":   "🔧  Editar Interfaz de Comunicación",
        "Português": "🔧  Editar Interface de Comunicação",
    },
    "builder.edit_clock": {
        "English":   "🔧  Edit Clock Frequency",
        "Español":   "🔧  Editar Frecuencia de Reloj",
        "Português": "🔧  Editar Frequência de Clock",
    },
    "builder.abort": {
        "English":   "❌  Abort",
        "Español":   "❌  Abortar",
        "Português": "❌  Abortar",
    },
    "builder.boot_no": {
        "English":   "No bootloader",
        "Español":   "Sin bootloader",
        "Português": "Sem bootloader",
    },
    "builder.boot_8k": {
        "English":   "8KiB bootloader",
        "Español":   "Bootloader de 8KiB",
        "Português": "Bootloader de 8KiB",
    },
    "builder.boot_16k": {
        "English":   "16KiB bootloader",
        "Español":   "Bootloader de 16KiB",
        "Português": "Bootloader de 16KiB",
    },
    "builder.boot_28k": {
        "English":   "28KiB bootloader",
        "Español":   "Bootloader de 28KiB",
        "Português": "Bootloader de 28KiB",
    },
    "builder.boot_32k": {
        "English":   "32KiB bootloader",
        "Español":   "Bootloader de 32KiB",
        "Português": "Bootloader de 32KiB",
    },
    "builder.boot_64k": {
        "English":   "64KiB bootloader",
        "Español":   "Bootloader de 64KiB",
        "Português": "Bootloader de 64KiB",
    },
    "builder.boot_128k": {
        "English":   "128KiB bootloader",
        "Español":   "Bootloader de 128KiB",
        "Português": "Bootloader de 128KiB",
    },
    "builder.enter_arch": {
        "English":   "Enter Kconfig Architecture (e.g. stm32, lpc176x):",
        "Español":   "Ingrese la Arquitectura de Kconfig (ej. stm32, lpc176x):",
        "Português": "Digite a Arquitetura do Kconfig (ex. stm32, lpc176x):",
    },
    "builder.enter_proc": {
        "English":   "Enter Processor Model (e.g. stm32f446):",
        "Español":   "Ingrese el Modelo del Procesador (ej. stm32f446):",
        "Português": "Digite o Modelo do Processador (ex. stm32f446):",
    },
    "builder.select_boot": {
        "English":   "Select Bootloader Offset:",
        "Español":   "Seleccione el Offset del Bootloader:",
        "Português": "Selecione o Offset do Bootloader:",
    },
    "builder.enter_manual": {
        "English":   "Enter manually",
        "Español":   "Ingresar manualmente",
        "Português": "Inserir manualmente",
    },
    "builder.enter_hex": {
        "English":   "Enter HEX offset (e.g. 0x8000):",
        "Español":   "Ingrese el offset HEX (ej. 0x8000):",
        "Português": "Digite o offset HEX (ex. 0x8000):",
    },
    "builder.select_interface": {
        "English":   "Select Interface:",
        "Español":   "Seleccione la Interfaz:",
        "Português": "Selecione a Interface:",
    },
    "builder.enter_clock": {
        "English":   "Enter Clock Frequency in Hz (e.g. 120000000):",
        "Español":   "Ingrese la Frecuencia de Reloj en Hz (ej. 120000000):",
        "Português": "Digite a Frequência de Clock em Hz (ex. 120000000):",
    },
    "builder.derivation_failed": {
        "English":   "Configuration derivation failed: {error}",
        "Español":   "La derivación de la configuración falló: {error}",
        "Português": "A derivação da configuração falhou: {error}",
    },
    "builder.compilation_aborted": {
        "English":   "Compilation aborted by user.",
        "Español":   "Compilación abortada por el usuario.",
        "Português": "Compilação abortada pelo usuário.",
    },
    "builder.no_binary": {
        "English":   "Firmware compiled, but no recognized output file (klipper.bin/.uf2/.elf.hex) found.",
        "Español":   "Firmware compilado, pero no se encontró ningún archivo de salida reconocido (klipper.bin/.uf2/.elf.hex).",
        "Português": "Firmware compilado, mas nenhum arquivo de saída reconhecido (klipper.bin/.uf2/.elf.hex) foi encontrado.",
    },
    "builder.make_error": {
        "English":   "Failed to compile firmware (Make error {code}):\n{error}",
        "Español":   "Error al compilar el firmware (Error de Make {code}):\n{error}",
        "Português": "Falha ao compilar o firmware (Erro do Make {code}):\n{error}",
    },
    "builder.make_not_found": {
        "English":   "Failed to compile firmware: 'make' command not found. build-essential package required.",
        "Español":   "Error al compilar el firmware: comando 'make' no encontrado. Se requiere el paquete build-essential.",
        "Português": "Falha ao compilar o firmware: comando 'make' não encontrado. Pacote build-essential necessário.",
    },
    "builder.unexpected_error": {
        "English":   "An unexpected error occurred during build: {error}",
        "Español":   "Ocurrió un error inesperado durante la compilación: {error}",
        "Português": "Ocorreu um erro inesperado durante a compilação: {error}",
    },
    # ── Macros strings ──────────────────────────────────────────
    "macro.pid_hotend.desc": {
        "English":   "PID Calibration for the hotend",
        "Español":   "Calibración PID para el hotend",
        "Português": "Calibração PID para o hotend",
    },
    "macro.pid_bed.desc": {
        "English":   "PID Calibration for the bed",
        "Español":   "Calibración PID para la cama",
        "Português": "Calibração PID para a mesa",
    },
    "macro.test_movement.desc": {
        "English":   "Test X and Y movement",
        "Español":   "Probar el movimiento en X e Y",
        "Português": "Testar o movimento em X e Y",
    },
    "macro.test_extruder.desc": {
        "English":   "Test extruder movement (hotend must be hot)",
        "Español":   "Probar el movimiento del extrusor (el hotend debe estar caliente)",
        "Português": "Testar o movimento da extrusora (o hotend deve estar quente)",
    },
    "macro.preheat_pla.desc": {
        "English":   "Preheat for PLA",
        "Español":   "Precalentar para PLA",
        "Português": "Preaquecer para PLA",
    },
    "macro.preheat_petg.desc": {
        "English":   "Preheat for PETG",
        "Español":   "Precalentar para PETG",
        "Português": "Preaquecer para PETG",
    },
    "macro.home_and_center.desc": {
        "English":   "Home all axes and center the toolhead",
        "Español":   "Hacer home en todos los ejes y centrar el cabezal",
        "Português": "Fazer home em todos os eixos e centralizar o cabeçote",
    },
    "macro.park_head.desc": {
        "English":   "Park the toolhead",
        "Español":   "Estacionar el cabezal",
        "Português": "Estacionar o cabeçote",
    },
    "macro.load_filament.desc": {
        "English":   "Load filament",
        "Español":   "Cargar filamento",
        "Português": "Carregar filamento",
    },
    "macro.unload_filament.desc": {
        "English":   "Unload filament",
        "Español":   "Descargar filamento",
        "Português": "Descarregar filamento",
    },
    "macro.print_start.desc": {
        "English":   "Start print procedure",
        "Español":   "Iniciar procedimiento de impresión",
        "Português": "Iniciar procedimento de impressão",
    },
    "macro.print_end.desc": {
        "English":   "End print procedure",
        "Español":   "Finalizar procedimiento de impresión",
        "Português": "Finalizar procedimento de impressão",
    },
    # ── Profile summary strings ──────────────────────────────────
    "profile.detected_header": {
        "English":   "Detected profile:",
        "Español":   "Perfil detectado:",
        "Português": "Perfil detectado:",
    },
    "profile.build_volume": {
        "English":   "Build volume",
        "Español":   "Volumen de impresión",
        "Português": "Volume de impressão",
    },
    "profile.kinematics": {
        "English":   "Kinematics",
        "Español":   "Cinemática",
        "Português": "Cinemática",
    },
    "profile.hotend_thermistor": {
        "English":   "Hotend thermistor",
        "Español":   "Termistor del hotend",
        "Português": "Termistor do hotend",
    },
    "profile.bed_thermistor": {
        "English":   "Bed thermistor",
        "Español":   "Termistor de la cama",
        "Português": "Termistor da mesa",
    },
    # ── Display Compatibility Layer strings ─────────────────────
    "display.warning_header": {
        "English":   "⚠️  Display Compatibility Warning",
        "Español":   "⚠️  Advertencia de Compatibilidad de Pantalla",
        "Português": "⚠️  Aviso de Compatibilidade de Display",
    },
    "display.status_supported": {
        "English":   "🟢 SUPPORTED",
        "Español":   "🟢 COMPATIBLE",
        "Português": "🟢 SUPORTADO",
    },
    "display.status_partial": {
        "English":   "🟡 PARTIAL SUPPORT",
        "Español":   "🟡 SOPORTE PARCIAL",
        "Português": "🟡 SUPORTE PARCIAL",
    },
    "display.status_unsupported": {
        "English":   "🔴 UNSUPPORTED",
        "Español":   "🔴 NO COMPATIBLE",
        "Português": "🔴 NÃO SUPORTADO",
    },
    "display.status_untested": {
        "English":   "⬜ UNTESTED",
        "Español":   "⬜ SIN PRUEBAS",
        "Português": "⬜ NÃO TESTADO",
    },
    "display.recommendation_disconnect": {
        "English":   "Recommendation: Physically disconnect the display from the mainboard",
        "Español":   "Recomendación: Desconecte físicamente la pantalla de la placa principal",
        "Português": "Recomendação: Desconecte fisicamente o display da placa principal",
    },
    "display.recommendation_optional": {
        "English":   "Recommendation: Display may have limited functionality — consider using the web UI instead",
        "Español":   "Recomendación: La pantalla puede tener funcionalidad limitada — considere usar la interfaz web",
        "Português": "Recomendação: O display pode ter funcionalidade limitada — considere usar a interface web",
    },
    "display.oem_explanation": {
        "English":   "OEM printer touchscreens are often designed specifically for Marlin firmware and may not function correctly under Klipper without additional community modifications.",
        "Español":   "Las pantallas táctiles de impresoras OEM generalmente están diseñadas específicamente para el firmware Marlin y pueden no funcionar correctamente en Klipper sin modificaciones adicionales de la comunidad.",
        "Português": "As telas touchscreen de impressoras OEM são frequentemente projetadas especificamente para o firmware Marlin e podem não funcionar corretamente com o Klipper sem modificações adicionais da comunidade.",
    },
    "display.web_ui_hint": {
        "English":   "💡 Mainsail and Fluidd provide full printer control from any phone, tablet, or PC — no physical screen required.",
        "Español":   "💡 Mainsail y Fluidd ofrecen control total de la impresora desde cualquier teléfono, tablet o PC — sin necesidad de pantalla física.",
        "Português": "💡 Mainsail e Fluidd oferecem controle total da impressora em qualquer telefone, tablet ou PC — sem necessidade de tela física.",
    },
    "display.docs_hint": {
        "English":   "📖 For full details, see: docs/en/DISPLAYS.md",
        "Español":   "📖 Para más detalles, consulte: docs/es/DISPLAYS.md",
        "Português": "📖 Para mais detalhes, consulte: docs/pt/DISPLAYS.md",
    },
    "display.continue_prompt": {
        "English":   "This printer may have display compatibility issues. Continue with configuration generation?",
        "Español":   "Esta impresora puede tener problemas de compatibilidad de pantalla. ¿Continuar con la generación de la configuración?",
        "Português": "Esta impressora pode ter problemas de compatibilidade de display. Continuar com a geração da configuração?",
    },
    "display.section_label": {
        "English":   "Detected section",
        "Español":   "Sección detectada",
        "Português": "Seção detectada",
    },
}


def t(key: str, **kwargs) -> str:
    """Look up a UI string by key in the current language.

    Falls back to English if the current language is missing a key,
    then falls back to the key string itself if no entry exists at all.
    Applies str.format(**kwargs) for dynamic substitutions.
    """
    lang = _current_lang
    entry = UI_STRINGS.get(key)
    if entry is None:
        return key.format(**kwargs) if kwargs else key
    text = entry.get(lang) or entry.get("English") or key
    return text.format(**kwargs) if kwargs else text


# ── Comment translation layer (unchanged) ─────────────────────

def translate_comment(comment, lang):
    if lang == "English":
        return comment

    translations = {
        "Serial connection to the printer controller board. Auto-detected by KACE. Verify in /dev/serial/by-id/ if connection fails.": {
            "Español": "Conexión serial a la placa controladora. Auto-detectado por KACE. Verifica en /dev/serial/by-id/ si falla.",
            "Português": "Conexão serial com a placa controladora. Auto-detectado pelo KACE. Verifique em /dev/serial/by-id/ se falhar."
        },
        "Printer kinematics type (cartesian, corexy, delta)": {
            "Español": "Tipo de cinemática de la impresora (cartesiana, corexy, delta)",
            "Português": "Tipo de cinemática da impressora (cartesiana, corexy, delta)"
        },
        "Maximum velocity (in mm/s) of the toolhead": {
            "Español": "Velocidad máxima (en mm/s) del cabezal",
            "Português": "Velocidade máxima (em mm/s) do cabeçote"
        },
        "Maximum acceleration (in mm/s^2) of the toolhead": {
            "Español": "Aceleración máxima (en mm/s^2) del cabezal",
            "Português": "Aceleração máxima (em mm/s^2) do cabeçote"
        },
        "Maximum velocity (in mm/s) of movement along the z axis": {
            "Español": "Velocidad máxima (en mm/s) del movimiento en el eje Z",
            "Português": "Velocidade máxima (em mm/s) de movimento no eixo Z"
        },
        "Maximum acceleration (in mm/s^2) of movement along the z axis": {
            "Español": "Aceleración máxima (en mm/s^2) en el eje Z",
            "Português": "Aceleração máxima (em mm/s^2) no eixo Z"
        },
        "Step pin for the X stepper driver": {
            "Español": "Pin de paso (step) para el motor X",
            "Português": "Pino de passo (step) para o motor X"
        },
        "Direction pin. Add or remove \"!\" to invert motor direction": {
            "Español": "Pin de dirección (dir). Agrega o quita \"!\" para invertir la dirección",
            "Português": "Pino de direção (dir). Adicione ou remova \"!\" para inverter a direção"
        },
        "Enable pin for the stepper driver": {
            "Español": "Pin de habilitación (enable) del motor",
            "Português": "Pino de habilitação (enable) do motor"
        },
        "Number of microsteps per full step": {
            "Español": "Número de micropasos por paso completo",
            "Português": "Número de micropassos por passo completo"
        },
        "Distance in mm the axis travels per full rotation of the motor": {
            "Español": "Distancia en mm que viaja el eje por cada rotación completa del motor",
            "Português": "Distância em mm que o eixo viaja por cada rotação completa do motor"
        },
        "Endstop pin. Add or remove \"!\" to invert logic": {
            "Español": "Pin de fin de carrera. Agrega o quita \"!\" para invertir la lógica",
            "Português": "Pino de fim de curso. Adicione ou remova \"!\" para inverter a lógica"
        },
        "Location of the endstop (usually 0)": {
            "Español": "Ubicación del fin de carrera (generalmente 0)",
            "Português": "Localização do fim de curso (geralmente 0)"
        },
        "Maximum valid X position": {
            "Español": "Posición máxima válida en X",
            "Português": "Posição máxima válida em X"
        },
        "Maximum velocity (in mm/s) of the stepper when homing": {
            "Español": "Velocidad máxima (en mm/s) del motor al hacer homing",
            "Português": "Velocidade máxima (em mm/s) do motor ao fazer homing"
        },
        "Step pin for the Y stepper driver": {
            "Español": "Pin de paso (step) para el motor Y",
            "Português": "Pino de passo (step) para o motor Y"
        },
        "Maximum valid Y position": {
            "Español": "Posición máxima válida en Y",
            "Português": "Posição máxima válida em Y"
        },
        "Step pin for the Z stepper driver": {
            "Español": "Pin de paso (step) para el motor Z",
            "Português": "Pino de passo (step) para o motor Z"
        },
        "Maximum valid Z position": {
            "Español": "Posición máxima válida en Z",
            "Português": "Posição máxima válida em Z"
        },
        "Step pin for the Z1 stepper driver": {
            "Español": "Pin de paso (step) para el motor Z1",
            "Português": "Pino de passo (step) para o motor Z1"
        },
        "Step pin for the extruder driver": {
            "Español": "Pin de paso (step) para el extrusor",
            "Português": "Pino de passo (step) para a extrusora"
        },
        "Pin connected to the hotend heater cartridge": {
            "Español": "Pin conectado al cartucho calentador del hotend",
            "Português": "Pino conectado ao cartucho de aquecimento do hotend"
        },
        "Pin connected to the hotend thermistor": {
            "Español": "Pin conectado al termistor del hotend",
            "Português": "Pino conectado ao termistor do hotend"
        },
        "Distance in mm the filament travels per full rotation of the motor": {
            "Español": "Distancia en mm que el filamento viaja por rotación del motor",
            "Português": "Distância em mm que o filamento viaja por rotação do motor"
        },
        "Diameter of the installed nozzle in mm": {
            "Español": "Diámetro de la boquilla instalada en mm",
            "Português": "Diâmetro do bico instalado em mm"
        },
        "Diameter of the filament being used": {
            "Español": "Diámetro del filamento que se está utilizando",
            "Português": "Diâmetro do filamento sendo utilizado"
        },
        "Type of thermistor used for the hotend": {
            "Español": "Tipo de termistor utilizado para el hotend",
            "Português": "Tipo de termistor utilizado para o hotend"
        },
        "Temperature control algorithm": {
            "Español": "Algoritmo de control de temperatura",
            "Português": "Algoritmo de controle de temperatura"
        },
        "PID proportional gain": {
            "Español": "Ganancia proporcional (PID)",
            "Português": "Ganho proporcional (PID)"
        },
        "PID integral gain": {
            "Español": "Ganancia integral (PID)",
            "Português": "Ganho integral (PID)"
        },
        "PID derivative gain": {
            "Español": "Ganancia derivativa (PID)",
            "Português": "Ganho derivativo (PID)"
        },
        "Minimum safe temperature": {
            "Español": "Temperatura mínima segura",
            "Português": "Temperatura mínima segura"
        },
        "Maximum safe temperature": {
            "Español": "Temperatura máxima segura",
            "Português": "Temperatura máxima segura"
        },
        "Pin connected to the probe sensor": {
            "Español": "Pin conectado al sensor del probe",
            "Português": "Pino conectado ao sensor do probe"
        },
        "Pin connected to the probe control": {
            "Español": "Pin conectado al control del probe",
            "Português": "Pino conectado ao controle do probe"
        },
        "Offset relative to the nozzle. Must be measured for your specific printer": {
            "Español": "Offset relativo a la boquilla. Debe medirse para tu impresora específica",
            "Português": "Offset relativo ao bico. Deve ser medido para sua impressora específica"
        },
        "Z offset should be calibrated using PROBE_CALIBRATE": {
            "Español": "El offset de Z debe calibrarse usando PROBE_CALIBRATE",
            "Português": "O offset de Z deve ser calibrado usando PROBE_CALIBRATE"
        },
        "XY position to move to before homing Z": {
            "Español": "Posición XY a la que moverse antes de hacer homing de Z",
            "Português": "Posição XY para a qual se mover antes de fazer homing de Z"
        },
        "Speed at which the toolhead is moved to the safe Z home coordinate": {
            "Español": "Velocidad a la que el cabezal se mueve hacia la coordenada de Z segura",
            "Português": "Velocidade em que o cabeçote é movido para a coordenada de Z segura"
        },
        "Distance (in mm) to lift the Z axis prior to homing": {
            "Español": "Distancia (mm) para levantar el eje Z antes de hacer homing",
            "Português": "Distância (mm) para levantar o eixo Z antes do homing"
        },
        "Speed (in mm/s) at which the Z axis is lifted prior to homing": {
            "Español": "Velocidad (en mm/s) a la que se levanta el eje Z antes del homing",
            "Português": "Velocidade (em mm/s) em que o eixo Z é levantado antes do homing"
        },
        "Pin connected to the heated bed solid state relay or MOSFET": {
            "Español": "Pin conectado al relé de estado sólido o MOSFET de la cama caliente",
            "Português": "Pino conectado ao relé de estado sólido ou MOSFET da mesa aquecida"
        },
        "Pin connected to the heated bed thermistor": {
            "Español": "Pin conectado al termistor de la cama caliente",
            "Português": "Pino conectado ao termistor da mesa aquecida"
        },
        "Type of thermistor used for the heated bed": {
            "Español": "Tipo de termistor utilizado para la cama caliente",
            "Português": "Tipo de termistor utilizado para a mesa aquecida"
        },
        "UART communication pin": {
            "Español": "Pin de comunicación UART",
            "Português": "Pino de comunicação UART"
        },
        "UART TX pin": {
            "Español": "Pin de TX UART",
            "Português": "Pino de TX UART"
        },
        "SPI chip select pin": {
            "Español": "Pin de selección de chip (CS) de SPI",
            "Português": "Pino de seleção de chip (CS) de SPI"
        },
        "SPI clock pin": {
            "Español": "Pin de reloj (SCK) de SPI",
            "Português": "Pino de relógio (SCK) de SPI"
        },
        "SPI MOSI pin": {
            "Español": "Pin MOSI de SPI",
            "Português": "Pino MOSI de SPI"
        },
        "SPI MISO pin": {
            "Español": "Pin MISO de SPI",
            "Português": "Pino MISO de SPI"
        },
        "SPI bus name": {
            "Español": "Nombre del bus SPI",
            "Português": "Nome do barramento SPI"
        },
        "Motor run current in amps": {
            "Español": "Corriente de funcionamiento del motor (Amperios)",
            "Português": "Corrente de funcionamento do motor (Amperes)"
        },
        "Motor hold current in amps": {
            "Español": "Corriente de retención del motor (Amperios)",
            "Português": "Corrente de retenção do motor (Amperes)"
        },
        "Set to 0 to use spreadCycle mode": {
            "Español": "Establecer en 0 para usar modo spreadCycle",
            "Português": "Defina como 0 para usar modo spreadCycle"
        },
        "Define aliases for board pins (e.g., EXP1 and EXP2 headers)": {
            "Español": "Define los alias para los pines de la placa (ej., conectores EXP1 y EXP2)",
            "Português": "Define os aliases para os pinos da placa (ex., conectores EXP1 e EXP2)"
        },
        "filament per motor revolution (mm) --- manual configuration --- (calibrate by extruding 100mm)": {
            "Español": "filamento por revolución del motor (mm) --- configuración manual --- (calibrar extruyendo 100mm)",
            "Português": "filamento por revolução do motor (mm) --- configuração manual --- (calibrar extrusando 100mm)"
        },
        "PID proportional --- manual configuration --- (run PID_CALIBRATE HEATER=extruder TARGET=200)": {
            "Español": "PID proporcional --- configuración manual --- (ejecutar PID_CALIBRATE HEATER=extruder TARGET=200)",
            "Português": "PID proporcional --- configuração manual --- (executar PID_CALIBRATE HEATER=extruder TARGET=200)"
        },
        "PID integral --- manual configuration --- (run PID_CALIBRATE)": {
            "Español": "PID integral --- configuración manual --- (ejecutar PID_CALIBRATE)",
            "Português": "PID integral --- configuração manual --- (executar PID_CALIBRATE)"
        },
        "PID derivative --- manual configuration --- (run PID_CALIBRATE)": {
            "Español": "PID derivativo --- configuración manual --- (ejecutar PID_CALIBRATE)",
            "Português": "PID derivativo --- configuração manual --- (executar PID_CALIBRATE)"
        },
        "distance from nozzle to probe in X (mm) --- manual configuration --- (measure physically from nozzle to probe tip)": {
            "Español": "distancia de la boquilla al sensor en X (mm) --- configuración manual --- (medir físicamente desde la boquilla hasta la punta del sensor)",
            "Português": "distância do bico ao sensor em X (mm) --- configuração manual --- (medir fisicamente do bico até a ponta do sensor)"
        },
        "distance from nozzle to probe in Y (mm) --- manual configuration --- (measure physically from nozzle to probe tip)": {
            "Español": "distancia de la boquilla al sensor en Y (mm) --- configuración manual --- (medir físicamente desde la boquilla hasta la punta del sensor)",
            "Português": "distância do bico ao sensor em Y (mm) --- configuração manual --- (medir fisicamente do bico até a ponta do sensor)"
        },
        "nozzle to bed distance (mm) --- manual configuration --- (set using PROBE_CALIBRATE)": {
            "Español": "distancia de la boquilla a la cama (mm) --- configuración manual --- (configurar usando PROBE_CALIBRATE)",
            "Português": "distância do bico à mesa (mm) --- configuração manual --- (configurar usando PROBE_CALIBRATE)"
        },
        "Probe speed in mm/s": {
            "Español": "Velocidad de prueba en mm/s",
            "Português": "Velocidade de teste em mm/s"
        },
        "Z height before moving to next probe point": {
            "Español": "Altura de Z antes de moverse al siguiente punto",
            "Português": "Altura de Z antes de mover para o próximo ponto"
        },
        "probing area start (mm) --- manual configuration --- (must be inside bed limits)": {
            "Español": "inicio del área de prueba (mm) --- configuración manual --- (debe estar dentro de los límites de la cama)",
            "Português": "início da área de teste (mm) --- configuração manual --- (deve estar dentro dos limites da mesa)"
        },
        "probing area end (mm) --- manual configuration --- (must be inside bed limits)": {
            "Español": "fin del área de prueba (mm) --- configuración manual --- (debe estar dentro de los límites de la cama)",
            "Português": "fim da área de teste (mm) --- configuração manual --- (deve estar dentro dos limites da mesa)"
        },
        "Probe grid size": {
            "Español": "Tamaño de la cuadrícula de prueba",
            "Português": "Tamanho da grade de teste"
        },
        "--- optional --- (automatic Z leveling for multiple motors)": {
            "Español": "--- opcional --- (nivelación automática de Z para múltiples motores)",
            "Português": "--- opcional --- (nivelamento automático de Z para múltiplos motores)"
        },
        "Locations of the bed pivot points": {
            "Español": "Ubicaciones de los puntos de pivote de la cama",
            "Português": "Localizações dos pontos de pivô da mesa"
        },
        "Probing points for Z leveling": {
            "Español": "Puntos de prueba para la nivelación de Z",
            "Português": "Pontos de teste para o nivelamento de Z"
        },
        "Speed of non-probing moves during leveling": {
            "Español": "Velocidad de movimientos sin prueba durante la nivelación",
            "Português": "Velocidade de movimentos sem teste durante o nivelamento"
        },
        "Z height to clear the bed when moving": {
            "Español": "Altura Z para despejar la cama al moverse",
            "Português": "Altura Z para limpar a mesa ao se mover"
        },
        "--- optional --- (for CoreXY gantry leveling)": {
            "Español": "--- opcional --- (para nivelación de pórtico CoreXY)",
            "Português": "--- opcional --- (para nivelamento de pórtico CoreXY)"
        },
        "Locations of the gantry pivot points": {
            "Español": "Ubicaciones de los puntos de pivote del pórtico",
            "Português": "Localizações dos pontos de pivô do pórtico"
        },
        "Probing points for gantry leveling": {
            "Español": "Puntos de prueba para la nivelación del pórtico",
            "Português": "Pontos de teste para o nivelamento do pórtico"
        },
        "bed PID proportional --- manual configuration --- (run PID_CALIBRATE HEATER=heater_bed TARGET=60)": {
            "Español": "PID proporcional de la cama --- configuración manual --- (ejecutar PID_CALIBRATE HEATER=heater_bed TARGET=60)",
            "Português": "PID proporcional da mesa --- configuração manual --- (executar PID_CALIBRATE HEATER=heater_bed TARGET=60)"
        },
        "bed PID integral --- manual configuration --- (run PID_CALIBRATE)": {
            "Español": "PID integral de la cama --- configuración manual --- (ejecutar PID_CALIBRATE)",
            "Português": "PID integral da mesa --- configuração manual --- (executar PID_CALIBRATE)"
        },
        "bed PID derivative --- manual configuration --- (run PID_CALIBRATE)": {
            "Español": "PID derivativo de la cama --- configuración manual --- (ejecutar PID_CALIBRATE)",
            "Português": "PID derivativo da mesa --- configuração manual --- (executar PID_CALIBRATE)"
        },
        "motor current (A) --- manual configuration --- (check motor specs)": {
            "Español": "corriente del motor (A) --- configuración manual --- (verificar especificaciones)",
            "Português": "corrente do motor (A) --- configuração manual --- (verificar especificações)"
        }
    }

    # If exact match exists
    if comment in translations and lang in translations[comment]:
        return translations[comment][lang]
        
    return comment
