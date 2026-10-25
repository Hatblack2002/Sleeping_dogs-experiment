import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_theoryengine.py"


class AuditScriptTests(unittest.TestCase):
    def test_generates_report_and_flags_pc_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "theory.hh").write_text(
                "#define THEORY_WINDOWS\n#define THEORY_PLATFORM_PC\n#include <d3d11.h>\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text("Reference tree for test", encoding="utf-8")
            (root / "quark").mkdir()
            (root / "quark" / "processplat.hh").write_text(
                "void process() { __debugbreak(); }\n", encoding="utf-8"
            )
            output = root / "report.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--source",
                    str(root),
                    "--output",
                    str(output),
                    "--revision",
                    "test-revision",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("test-revision", report)
            self.assertIn("Direct3D 11 headers or symbols", report)
            self.assertIn("Windows API / platform headers", report)
            self.assertIn("No top-level LICENSE/LICENCE/COPYING file found", report)
            self.assertIn("Wrote", result.stdout)

    def test_missing_source_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "does-not-exist"
            output = Path(temp) / "report.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--source",
                    str(missing),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source directory does not exist", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
