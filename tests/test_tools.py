"""Tests use synthetic JSON, never network benchmark measurements."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


iperf = load("summarize_iperf")
collector = load("collect_environment")
docs = load("check_docs")


def tcp():
    return {
        "start": {"test_start": {"protocol": "TCP", "reverse": 0, "num_streams": 1}},
        "end": {
            "sum_sent": {"bits_per_second": 12000000, "retransmits": 4},
            "sum_received": {"bits_per_second": 10000000, "seconds": 10, "bytes": 12500000},
        },
    }


class IperfTests(unittest.TestCase):
    def test_uses_receiver_not_sender(self):
        row = iperf.summarize(tcp())
        self.assertEqual(row["receiver_mbps"], 10)
        self.assertEqual(row["sender_retransmits"], 4)
        self.assertIsNone(row["receiver_lost_percent"])

    def test_reverse_keeps_receiver_semantics(self):
        data = tcp()
        data["start"]["test_start"]["reverse"] = 1
        self.assertTrue(iperf.summarize(data)["reverse"])
        self.assertEqual(iperf.summarize(data)["receiver_mbps"], 10)

    def test_udp_explicit_legacy_receiver(self):
        data = {
            "start": {"test_start": {"protocol": "UDP"}},
            "end": {"sum": {"sender": False, "bits_per_second": 8000000,
                            "seconds": 5, "packets": 1000, "lost_packets": 10,
                            "lost_percent": 1, "jitter_ms": 0.25}},
        }
        row = iperf.summarize(data)
        self.assertEqual(row["receiver_lost_percent"], 1)
        self.assertEqual(row["receiver_source"], "end.sum")
        self.assertEqual(row["receiver_jitter_ms"], 0.25)
        self.assertIsNone(row["sender_retransmits"])

    def test_udp_new_receiver(self):
        data = tcp()
        data["start"]["test_start"]["protocol"] = "UDP"
        data["end"]["sum_received"]["lost_percent"] = 0
        self.assertEqual(iperf.summarize(data)["receiver_lost_percent"], 0)

    def test_rejects_ambiguous_udp(self):
        data = {"start": {"test_start": {"protocol": "UDP"}},
                "end": {"sum": {"seconds": 2, "bits_per_second": 100}}}
        with self.assertRaises(ValueError):
            iperf.summarize(data)

    def test_does_not_fallback_to_sent(self):
        data = tcp()
        del data["end"]["sum_received"]
        with self.assertRaises(ValueError):
            iperf.summarize(data)

    def test_errors_bidir_zero_nan_rejected(self):
        for kind in ("error", "bidir", "zero", "nan"):
            with self.subTest(kind=kind):
                data = tcp()
                if kind == "error":
                    data["error"] = "connection failed"
                elif kind == "bidir":
                    data["start"]["test_start"]["bidir"] = 1
                elif kind == "zero":
                    data["end"]["sum_received"]["seconds"] = 0
                else:
                    data["end"]["sum_received"]["bits_per_second"] = float("nan")
                with self.assertRaises(ValueError):
                    iperf.summarize(data)

    def test_cli_no_partial_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = Path(tmp) / "good.json", Path(tmp) / "bad.json"
            good.write_text(json.dumps(tcp()), encoding="utf-8")
            bad.write_text('{"error": "failure"}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/summarize_iperf.py"), str(good), str(bad)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")

    def test_cli_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tcp.json"
            path.write_text(json.dumps(tcp()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/summarize_iperf.py"), "--format", "csv", str(path)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("receiver_mbps", result.stdout)
            self.assertIn("10.0", result.stdout)


class SafetyAndDocsTests(unittest.TestCase):
    def test_invalid_interface_creates_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "new"
            with self.assertRaises(ValueError):
                collector.collect("../bad", target)
            self.assertFalse(target.exists())

    @unittest.skipUnless(Path("/sys/class/net/lo").exists(), "Linux loopback required")
    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            sentinel = Path(tmp) / "sentinel"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                collector.collect("lo", tmp)
            self.assertEqual(sentinel.read_text(), "keep")

    def test_checker_detects_missing_link_and_fence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[bad](missing.md)\n\n" + chr(96) * 3 + "bash\n",
                                           encoding="utf-8")
            _, errors = docs.check(root)
            self.assertEqual(len(errors), 2)


if __name__ == "__main__":
    unittest.main()
