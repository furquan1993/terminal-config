"""Offline regression tests; all credentials are synthetic."""
import importlib.util
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('import_cookies.py')
spec = importlib.util.spec_from_file_location('import_cookies', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CookieTests(unittest.TestCase):
    def test_fragmented_cookie_and_equals(self):
        data, count = module.cookie_rows('Cookie: AWSELBAuthSessionCookie-0=abc==; AWSELBAuthSessionCookie-1=def', 'kibana.example.com')
        self.assertEqual(count, 2)
        self.assertIn('kibana.example.com\tFALSE\t/\tTRUE\t0\tAWSELBAuthSessionCookie-0\tabc==\n', data)

    def test_invalid_input(self):
        for raw in ['', 'curl --url https://example.com', 'a=1\nb=2', 'a=1; a=2', 'a=1; malformed', 'a=1\tb=2']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                module.cookie_rows(raw, 'example.com')

    def test_private_atomic_refresh_and_no_leaks(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'cookies.txt'
            command = [sys.executable, str(SCRIPT), '--stdin', '--output', str(target)]
            for token in ['SYNTHETIC_FIRST', 'SYNTHETIC_SECOND']:
                result = subprocess.run(command, input='session=' + token, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0)
                self.assertNotIn(token, result.stdout + result.stderr)
                self.assertIn(token, target.read_text())
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
            previous = target.read_bytes()
            result = subprocess.run(command, input='INVALID_SECRET', text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('INVALID_SECRET', result.stdout + result.stderr)
            self.assertEqual(target.read_bytes(), previous)

    def test_symlink_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / 'original'
            original.write_text('unchanged')
            link = Path(directory) / 'link'
            link.symlink_to(original)
            with self.assertRaises(ValueError):
                module.save_private(link, 'secret')
            self.assertEqual(original.read_text(), 'unchanged')

    def test_usage_error_does_not_echo_secrets(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--cookie', 'SYNTHETIC_SECRET'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('SYNTHETIC_SECRET', result.stdout + result.stderr)

    def test_prompt_refuses_noninteractive_input(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--prompt'], input='SYNTHETIC_SECRET', capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('SYNTHETIC_SECRET', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
