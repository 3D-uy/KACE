# core/translations.py

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
        }
    }

    # If exact match exists
    if comment in translations and lang in translations[comment]:
        return translations[comment][lang]
        
    return comment
