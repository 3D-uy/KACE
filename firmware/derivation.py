from .prompts import prompt_communication_interface, prompt_bootloader_offset, prompt_mcu_family

def derive_config(mcu, hint=None):
    """
    Intelligently builds Kconfig parameters based on patterns in the MCU string.
    Replaces massive static dictionaries with fallback inferencing logic.
    """
    config = {
        "CONFIG_LOW_LEVEL_OPTIONS": "y"
    }

    if mcu:
        mcu = str(mcu).lower()

    # 1. Derive Architecture, Family and Bootloader offsets
    if mcu is None:
        arch = prompt_mcu_family()
        config["CONFIG_MCU"] = f'"{arch}"'
        if arch != "linux":
            print("Make sure to manually configure other specific settings like bootloader.")
    elif "stm32f1" in mcu:
        config["CONFIG_MCU"] = '"stm32"'
        config["CONFIG_MACH_STM32"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        config["CONFIG_FLASH_START"] = "0x7000" if "103" in mcu else "0x0"
    elif "stm32f4" in mcu:
        config["CONFIG_MCU"] = '"stm32"'
        config["CONFIG_MACH_STM32"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        config["CONFIG_FLASH_START"] = "0x8000"
    elif "stm32h7" in mcu:
        config["CONFIG_MCU"] = '"stm32"'
        config["CONFIG_MACH_STM32"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        config["CONFIG_FLASH_START"] = "0x20000"
    elif "stm32g0b" in mcu:
        config["CONFIG_MCU"] = '"stm32"'
        config["CONFIG_MACH_STM32"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        config["CONFIG_FLASH_START"] = "0x2000"
    elif "stm32" in mcu:
        # Fallback STM32 without clear flash mappings
        config["CONFIG_MCU"] = '"stm32"'
        config["CONFIG_MACH_STM32"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        
        # Ambiguous bootloader, ask user
        options = {
            "No bootloader (0x0)": "0x0",
            "8KiB bootloader (0x2000)": "0x2000",
            "28KiB bootloader (0x7000)": "0x7000",
            "32KiB bootloader (0x8000)": "0x8000",
            "64KiB bootloader (0x10000)": "0x10000",
            "128KiB bootloader (0x20000)": "0x20000"
        }
        res = prompt_bootloader_offset(mcu, options)
        if res != "0x0":
            config["CONFIG_FLASH_START"] = res

    elif "lpc176" in mcu:
        config["CONFIG_MCU"] = '"lpc176x"'
        config["CONFIG_MACH_LPC176X"] = "y"
        config[f"CONFIG_MCU_{mcu.upper()}"] = "y"
        config["CONFIG_FLASH_START"] = "0x4000"
        if "69" in mcu:
            config["CONFIG_CLOCK_FREQ"] = "120000000"
        elif "68" in mcu:
            config["CONFIG_CLOCK_FREQ"] = "100000000"
            
    elif "rp2040" in mcu:
        config["CONFIG_MCU"] = '"rp2040"'
        config["CONFIG_MACH_RP2040"] = "y"

    elif "avr" in mcu or "atmega" in mcu:
        config["CONFIG_MCU"] = '"avr"'
        config["CONFIG_MACH_AVR"] = "y"
        if "2560" in mcu:
            config["CONFIG_MCU_ATMEGA2560"] = "y"

    elif mcu == "linux" or "host" in mcu:
        config["CONFIG_MCU"] = '"linux"'
        return config # Linux doesn't need interfaces or bootloaders

    else:
        # Unknown MCU pattern
        raise ValueError("Unknown MCU model")
        
    # 2. Derive Communication interface
    comm = hint
    if not hint or hint not in ["usb", "uart", "can", "spi", "tty"]:
         ans = prompt_communication_interface(mcu if mcu else "Board")
         comm = ans.lower() if ans else "usb"

    if comm == "usb":
         config["CONFIG_USB"] = "y"
         config["CONFIG_SERIAL"] = "n"
         config["CONFIG_CANBUS"] = "n"
    elif comm == "can":
         config["CONFIG_CANBUS"] = "y"
         config["CONFIG_USB"] = "n"
         config["CONFIG_SERIAL"] = "n"
    elif comm in ["uart", "tty"]:
         config["CONFIG_SERIAL"] = "y" 
         config["CONFIG_USB"] = "n"
         config["CONFIG_CANBUS"] = "n"
    elif comm == "spi":
         config["CONFIG_SPI"] = "y"

    return config
