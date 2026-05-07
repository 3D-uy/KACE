import unittest
import os
from tests.kace_test_case import KaceTestCase
from core.scraper import parse_config, extract_profile_defaults
from core.generator import generate_config

# Mock Klipper config representing generic-bigtreetech-skr-v1.4.cfg
MOCK_SKR14_RAW_CONFIG = """
# This file contains common pin mappings for the BIGTREETECH SKR V1.4
# board. To use this config, the firmware should be compiled for the
# LPC1768 or LPC1769(Turbo).

[stepper_x]
step_pin: P2.2
dir_pin: !P2.6
enable_pin: !P2.1
microsteps: 16
rotation_distance: 40
endstop_pin: P1.29
position_endstop: 0
position_max: 235
homing_speed: 50

[stepper_y]
step_pin: P0.19
dir_pin: !P0.20
enable_pin: !P2.8
microsteps: 16
rotation_distance: 40
endstop_pin: P1.28
position_endstop: 0
position_max: 235
homing_speed: 50

[stepper_z]
step_pin: P0.22
dir_pin: P2.11
enable_pin: !P0.21
microsteps: 16
rotation_distance: 8
endstop_pin: P1.27
position_endstop: 0.0
position_max: 300

[extruder]
step_pin: P2.13
dir_pin: !P0.11
enable_pin: !P2.12
microsteps: 16
rotation_distance: 33.500
nozzle_diameter: 0.400
filament_diameter: 1.750
heater_pin: P2.7
sensor_type: EPCOS 100K B57560G104F
sensor_pin: P0.24
control: pid
pid_Kp: 22.2
pid_Ki: 1.08
pid_Kd: 114
min_temp: 0
max_temp: 260

[heater_bed]
heater_pin: P2.5
sensor_type: EPCOS 100K B57560G104F
sensor_pin: P0.25
control: pid
pid_Kp: 54.027
pid_Ki: 0.770
pid_Kd: 948.182
min_temp: 0
max_temp: 130

[mcu]
serial: /dev/serial/by-id/usb-Klipper_Klipper_firmware_12345-if00

[printer]
kinematics: cartesian
max_velocity: 400
max_accel: 500
max_z_velocity: 10
max_z_accel: 100
"""

class TestConfigGeneration(KaceTestCase):

    def test_skr14_snapshot(self):
        """Regression test for generating a complete printer.cfg for an SKR v1.4."""
        
        # 1. Parse raw config
        parsed = parse_config(MOCK_SKR14_RAW_CONFIG, "generic-bigtreetech-skr-v1.4.cfg")
        defaults = extract_profile_defaults(parsed)

        # 2. Mock user wizard data
        user_data = {
            "mcu_path": "/dev/serial/by-id/usb-Klipper_lpc1769_mock-if00",
            "kinematics": defaults["kinematics"],
            "x_size": "235",
            "y_size": "235",
            "z_size": "250",
            "stepper_drivers": "TMC2209",
            "hotend_thermistor": defaults["hotend_thermistor"],
            "bed_thermistor": defaults["bed_thermistor"],
            "probe": "BLTouch",
            "motors": "4",
            "z_motors": "1",
            "extruder": "1",
            "runout": "Yes",
            "language": "en"
        }

        # 3. Set up KACE env for templates
        kace_dir = os.path.join(os.path.dirname(__file__), "..", "..")
        kace_dir = os.path.abspath(kace_dir)
        
        # Temporary output path
        output_file = os.path.join(kace_dir, "tests", "fixtures", "printer.cfg.temp")

        # 4. Generate
        try:
            generate_config(parsed, user_data, output_path=output_file)
            
            # Read output
            with open(output_file, "r", encoding="utf-8") as f:
                actual_cfg = f.read()
                
            # 5. Snapshot Assertion
            self.assertSnapshot("skr-v1.4-expected", actual_cfg)
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
