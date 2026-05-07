import unittest
import os

class KaceTestCase(unittest.TestCase):
    """Base class for KACE tests, providing snapshot utilities."""
    
    @classmethod
    def setUpClass(cls):
        # Ensure fixtures directory exists
        cls.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        os.makedirs(cls.fixtures_dir, exist_ok=True)

    def assertSnapshot(self, snapshot_name, actual_content):
        """
        Compare actual content against a saved snapshot.
        If KACE_UPDATE_SNAPSHOTS environment variable is set, it overwrites the snapshot.
        """
        snapshot_path = os.path.join(self.fixtures_dir, f"{snapshot_name}.txt")
        
        # Check if we should update snapshots
        if os.environ.get('KACE_UPDATE_SNAPSHOTS') == '1':
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(actual_content)
            self.skipTest(f"Updated snapshot for {snapshot_name}")
            return

        # Regular assertion
        self.assertTrue(os.path.exists(snapshot_path), f"Snapshot {snapshot_name} not found. Run with --update-snapshots to create it.")
        
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            expected_content = f.read()

        # Clean up whitespace for stable comparison
        expected = "\n".join([line.rstrip() for line in expected_content.splitlines()]).strip()
        actual = "\n".join([line.rstrip() for line in actual_content.splitlines()]).strip()

        self.assertEqual(expected, actual, f"Snapshot mismatch for {snapshot_name}")
