import unittest
import sys
import subprocess
import builtins
from core.deployer import _require_paramiko

class TestDeployer(unittest.TestCase):

    def test_lazy_paramiko_offline_handling(self):
        """Simulate a network failure during pip install of paramiko."""
        
        # Save originals
        orig_check_output = subprocess.check_output
        orig_print = builtins.print
        orig_paramiko = sys.modules.get('paramiko')

        # Mock a CalledProcessError representing a network failure
        def mock_check_output(*args, **kwargs):
            raise subprocess.CalledProcessError(
                returncode=1,
                cmd=args[0],
                output=b"NewConnectionError: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution"
            )

        subprocess.check_output = mock_check_output
        sys.modules['paramiko'] = None  # Force ImportError

        logs = []
        def mock_print(*args, **kwargs):
            logs.append(" ".join(map(str, args)))
        builtins.print = mock_print

        try:
            result = _require_paramiko()
            self.assertIsNone(result, "Should return None on installation failure")
            self.assertTrue(any("Network unreachable" in log for log in logs), "Did not detect network error")
        finally:
            # Restore originals
            subprocess.check_output = orig_check_output
            builtins.print = orig_print
            if orig_paramiko is not None:
                sys.modules['paramiko'] = orig_paramiko
            else:
                del sys.modules['paramiko']

if __name__ == '__main__':
    unittest.main()
