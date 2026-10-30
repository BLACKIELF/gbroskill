# SPDX-License-Identifier: MIT
"""Safety checks for unsupported hosts and incomplete model transfers."""
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate
import preflight


class PreflightTests(unittest.TestCase):
    def test_real_host_cli_without_model_reports_missing_readiness(self):
        result = subprocess.run([sys.executable, str(Path(preflight.__file__))], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertFalse(report['voice']['can_generate'])
        self.assertEqual(report['voice']['runtime']['system'], platform.system())
        self.assertFalse(report['network_requests'])
        self.assertFalse(report['audio_generated'])

    def test_linux_cannot_be_reported_ready(self):
        with patch('preflight.platform.system', return_value='Linux'), patch('preflight.platform.machine', return_value='x86_64'):
            result = preflight.runtime_environment()
        self.assertFalse(result['verified_platform_match'])
        self.assertFalse(result['metal_available'])
        self.assertFalse(result['ready'])

    def test_model_transfer_must_be_complete_and_unchanged(self):
        payload = b'fixed model fixture'
        manifest = {'files': [{'path': 'weights.bin', 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}]}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertFalse(preflight.verify_model(root, manifest)['ok'])
            (root / 'weights.bin').write_bytes(payload)
            self.assertTrue(preflight.verify_model(root, manifest)['ok'])
            (root / 'weights.bin').write_bytes(b'x' * len(payload))
            self.assertFalse(preflight.verify_model(root, manifest)['ok'])

    def test_unready_generation_does_not_write_audio_or_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'model.safetensors').write_bytes(b'not a model')
            (root / 'script.txt').write_text('Approved complete narration.', encoding='utf-8')
            output = root / 'speech.wav'
            args = ['generate.py', '--model', str(root), '--text-file', str(root / 'script.txt'), '--output', str(output)]
            with patch.object(sys, 'argv', args), patch('preflight.inspect_environment', return_value={'voice': {'can_generate': False}}):
                with self.assertRaises(SystemExit) as result:
                    generate.main()
            self.assertIn('voice_runtime_not_ready', str(result.exception))
            self.assertFalse(output.exists())
            self.assertFalse(output.with_suffix('.json').exists())


if __name__ == '__main__':
    unittest.main()
