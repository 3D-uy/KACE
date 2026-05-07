import unittest
from core.scraper import parse_config

class TestScraper(unittest.TestCase):

    def test_bltouch_injection(self):
        """Ensure BLTouch pins are correctly injected based on filename matching."""
        
        # Pass empty config data and SKR v1.4 filename
        result = parse_config('', 'generic-bigtreetech-skr-v1.4.cfg')
        
        self.assertIn('bltouch', result)
        self.assertEqual(result['bltouch'].get('sensor_pin'), '^P0.10')
        self.assertEqual(result['bltouch'].get('control_pin'), 'P2.0')

if __name__ == '__main__':
    unittest.main()
