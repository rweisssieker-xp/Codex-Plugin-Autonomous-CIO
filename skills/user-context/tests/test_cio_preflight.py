import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cio_preflight.py"


class CIOPreflightTests(unittest.TestCase):
    def test_preflight_without_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["CODEX_HOME"] = tmp
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--workflow", "index"],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            data = json.loads(proc.stdout)["cio_preflight"]
            self.assertEqual(data["workflow"], "index")
            self.assertEqual(data["user_context"]["status"], "missing")
            self.assertTrue(data["sources"])
            self.assertTrue(data["final_obligations"])

    def test_preflight_with_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state" / "plugins" / "the-autonomous-cio" / "the-autonomous-cio"
            state.mkdir(parents=True)
            (state / "user-context.md").write_text(
                "# Board Preferences\n\n- Use a one-page decision-first format.\n",
                encoding="utf-8",
            )
            env = dict(os.environ)
            env["CODEX_HOME"] = tmp
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--workflow", "executive-decision-packet"],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            data = json.loads(proc.stdout)["cio_preflight"]
            self.assertEqual(data["user_context"]["status"], "loaded")
            self.assertEqual(data["user_context"]["entries"][0]["category"], "Board Preferences")


if __name__ == "__main__":
    unittest.main()
