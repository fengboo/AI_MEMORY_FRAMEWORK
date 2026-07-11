import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from diagnostics import Diagnostic, should_fail, summary


class DiagnosticTests(unittest.TestCase):
    def test_severity_summary_and_exit(self):
        items = [Diagnostic("X", "info", "i"), Diagnostic("Y", "warning", "w")]
        self.assertEqual(summary(items, 2), {"scanned": 2, "errors": 0, "warnings": 1, "info": 1})
        self.assertFalse(should_fail(items))
        self.assertTrue(should_fail(items, fail_on_warning=True))

    def test_bridge_deprecated_template_is_non_failing_info(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "bridge_config_check.py"), "--all", "--json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["summary"]["errors"], 0)
        self.assertGreaterEqual(payload["summary"]["info"], 1)

    def test_stale_lint_warning_only_and_fail_on_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); context = root / "AI_CONTEXT"; context.mkdir()
            (context / "item.md").write_text("---\ntype: policy\nscope: global\nstatus: active\nlast_updated: 2000-01-01\n---\n# old\n", encoding="utf-8")
            base = [sys.executable, str(SCRIPTS / "ai_context_lint.py"), "--root", str(root), "--strict", "--json"]
            result = subprocess.run(base, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["summary"]["warnings"], 1)
            result = subprocess.run(base + ["--fail-on-warning"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
