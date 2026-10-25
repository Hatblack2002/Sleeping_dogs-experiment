import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "probe_android_header.py"


class AndroidHeaderProbeTests(unittest.TestCase):
    def test_compiler_failure_is_reported_without_failing_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            sysroot = root / "sysroot"
            source.mkdir()
            sysroot.mkdir()
            compiler = root / "fake-clang"
            compiler.write_text(
                "#!/bin/sh\ncat >/dev/null\necho 'fatal error: d3d11.h not found' >&2\nexit 1\n",
                encoding="utf-8",
            )
            compiler.chmod(0o755)
            output = root / "probe.md"
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPT),
                    "--compiler", str(compiler),
                    "--source", str(source),
                    "--sysroot", str(sysroot),
                    "--output", str(output),
                ],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("Status: **FAIL**", report)
            self.assertIn("d3d11.h not found", report)
            self.assertIn("does not produce an APK", report)

    def test_missing_sysroot_is_a_configuration_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPT),
                    "--compiler", "clang++",
                    "--source", str(source),
                    "--sysroot", str(root / "missing"),
                    "--output", str(root / "probe.md"),
                ],
                check=False, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Android NDK sysroot does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
