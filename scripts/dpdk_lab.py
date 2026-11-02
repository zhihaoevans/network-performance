#!/usr/bin/env python3
"""Unprivileged DPDK lab launcher: no PCI, hugepages or host network changes."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def command(mode, cpus):
    needed = 2 if mode == "null" else 1
    if len(cpus) < needed:
        raise ValueError(f"{mode} requires {needed} allowed logical CPUs")
    mapping = ",".join(f"{i}@{cpu}" for i, cpu in enumerate(cpus[:needed]))
    eal = ["--lcores", mapping, "--main-lcore", "0",
           "--no-huge", "--no-pci", "--no-shconf", "--iova-mode=va",
           "--no-telemetry", "-m", "256"]
    if mode == "null":
        return ["dpdk-testpmd", *eal, "--vdev=net_null0", "--vdev=net_null1",
                "--", "-i", "--nb-cores=1", "--rxq=1", "--txq=1",
                "--rxd=128", "--txd=128", "--total-num-mbufs=4096",
                "--mbcache=128", "--no-numa", "--forward-mode=io"]
    if mode == "hello":
        return ["/opt/dpdk-src/build/examples/dpdk-helloworld", *eal]
    if mode == "mbuf":
        return [str(ROOT / "examples/dpdk-mbuf/build/mbuf-demo"), *eal]
    raise ValueError("unknown lab mode")


def smoke(argv, seconds=2, startup_timeout=30):
    with tempfile.TemporaryDirectory(prefix="dpdk-smoke-") as tmp:
        path = Path(tmp) / "testpmd.log"
        with path.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=log,
                                       stderr=subprocess.STDOUT, text=True)
            try:
                deadline = time.monotonic() + startup_timeout
                # Wait for initialization, rather than counting startup as forwarding time.
                ready = False
                while process.poll() is None and time.monotonic() < deadline:
                    if "testpmd>" in path.read_text(encoding="utf-8", errors="replace"):
                        ready = True
                        break
                    time.sleep(0.05)
                if ready:
                    process.stdin.write("start\n")
                    process.stdin.flush()
                    time.sleep(seconds)
                    process.communicate("stop\nshow port stats all\nquit\n", timeout=30)
                else:
                    process.kill()
                    process.communicate()
            except (BrokenPipeError, subprocess.TimeoutExpired):
                process.kill()
                process.communicate()
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        output = path.read_text(encoding="utf-8", errors="replace")
    counts = [int(n) for n in re.findall(r"RX-packets:\s*(\d+)", output)]
    ok = process.returncode == 0 and bool(counts) and sum(counts) > 0
    return ok, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("null", "hello", "mbuf"))
    parser.add_argument("--smoke", action="store_true", help="bounded NULL-PMD functional test")
    parser.add_argument("--dry-run", action="store_true", help="print argv without running")
    args = parser.parse_args()
    if args.smoke and args.mode != "null":
        parser.error("--smoke is only supported for null")
    if not hasattr(os, "sched_getaffinity"):
        parser.error("Linux sched_getaffinity is required")
    try:
        argv = command(args.mode, sorted(os.sched_getaffinity(0)))
    except ValueError as exc:
        parser.error(str(exc))
    if args.dry_run:
        print(json.dumps(argv, ensure_ascii=False))
        return 0
    if shutil.which(argv[0]) is None:
        parser.exit(2, f"Executable not found: {argv[0]}. Build/rebuild the dev container first.\n")
    if args.smoke:
        ok, output = smoke(argv)
        print(output, end="")
        if not ok:
            parser.exit(1, "NULL PMD self-check failed: need a clean exit and positive RX counters.\n")
        print("PASS: NULL PMD produced packets. This is NOT a NIC performance measurement.")
        return 0
    return subprocess.call(argv)


if __name__ == "__main__":
    sys.exit(main())
