"""Launcher tests use a fake child, not a DPDK performance result."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("dpdk_lab", ROOT / "scripts/dpdk_lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class LauncherTests(unittest.TestCase):
    def test_nonzero_high_cpu_ids(self):
        argv = lab.command("null", [150, 151])
        self.assertEqual(argv[argv.index("--lcores") + 1], "0@150,1@151")
        self.assertIn("--no-huge", argv)
        self.assertIn("--no-pci", argv)
        self.assertIn("--no-shconf", argv)
        self.assertNotIn("--in-memory", argv)

    def test_two_cpus_required_for_null(self):
        with self.assertRaises(ValueError):
            lab.command("null", [4])

    def test_hello_can_run_with_one_cpu(self):
        argv = lab.command("hello", [8])
        self.assertEqual(argv[argv.index("--lcores") + 1], "0@8")

    def test_mbuf_binary_path(self):
        self.assertTrue(lab.command("mbuf", [1])[0].endswith("examples/dpdk-mbuf/build/mbuf-demo"))

    def fake_smoke(self, count, status=0):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fake.py"
            path.write_text(
                "import sys\n"
                "print('testpmd> ', end='', flush=True)\n"
                "for line in sys.stdin:\n"
                "    if line.strip() == 'quit':\n"
                "        break\n"
                f"print('RX-packets: {count}')\n"
                f"sys.exit({status})\n", encoding="utf-8")
            return lab.smoke([sys.executable, str(path)], seconds=0.01)

    def test_smoke_requires_positive_rx(self):
        ok, _ = self.fake_smoke(0)
        self.assertFalse(ok)

    def test_smoke_requires_clean_exit(self):
        ok, _ = self.fake_smoke(100, 1)
        self.assertFalse(ok)

    def test_smoke_passes_for_clean_positive_rx(self):
        ok, output = self.fake_smoke(100)
        self.assertTrue(ok)
        self.assertIn("RX-packets: 100", output)

    def test_smoke_rejects_unready_child(self):
        ok, _ = lab.smoke(
            [sys.executable, "-c", "import time; time.sleep(5)"],
            seconds=0.01, startup_timeout=0.1)
        self.assertFalse(ok)

    def test_dry_run_needs_no_dpdk(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/dpdk_lab.py"), "hello", "--dry-run"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--no-pci", result.stdout)


if __name__ == "__main__":
    unittest.main()
