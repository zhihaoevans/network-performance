#!/usr/bin/env python3
"""Read-only Linux network inventory; never changes network configuration."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


def collect(interface, output, timeout=5):
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", interface) or interface.startswith("-"):
        raise ValueError("invalid interface name")
    if not (Path("/sys/class/net") / interface).is_dir():
        raise ValueError("interface not found in this network namespace")
    output = Path(output)
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    commands = [
        ("kernel", ["uname", "-a"]),
        ("cpu", ["lscpu"]),
        ("numa", ["numactl", "--hardware"]),
        ("link", ["ip", "-s", "-s", "link", "show", "dev", interface]),
        ("driver", ["ethtool", "-i", interface]),
        ("rings", ["ethtool", "-g", interface]),
        ("channels", ["ethtool", "-l", interface]),
        ("coalesce", ["ethtool", "-c", interface]),
        ("offloads", ["ethtool", "-k", interface]),
        ("nic_stats", ["ethtool", "-S", interface]),
        ("rss", ["ethtool", "-x", interface]),
        ("qdisc", ["tc", "-s", "qdisc", "show", "dev", interface]),
        ("protocol", ["nstat", "-az"]),
    ]
    manifest = {
        "schema_version": 1, "interface": interface,
        "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": "read-only", "commands": [], "files": [],
    }
    env = dict(os.environ, LC_ALL="C")
    for name, argv in commands:
        item = {"name": name, "argv": argv}
        started = time.monotonic()
        if not shutil.which(argv[0]):
            item["status"] = "missing-command"
        else:
            try:
                with (output / (name + ".txt")).open("x", encoding="utf-8") as stream:
                    result = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT,
                                            timeout=timeout, check=False, env=env)
                item.update(status="ok" if result.returncode == 0 else "failed",
                            returncode=result.returncode, file=name + ".txt")
            except subprocess.TimeoutExpired:
                item.update(status="timeout", file=name + ".txt")
            except OSError as exc:
                item.update(status="failed", error=str(exc))
        item["elapsed_seconds"] = round(time.monotonic() - started, 3)
        manifest["commands"].append(item)
    sources = {
        "interrupts": Path("/proc/interrupts"),
        "softirqs": Path("/proc/softirqs"),
        "softnet_stat": Path("/proc/net/softnet_stat"),
        "meminfo": Path("/proc/meminfo"),
        "nic_numa_node": Path("/sys/class/net") / interface / "device/numa_node",
    }
    for name, path in sources.items():
        item = {"name": name, "source": str(path)}
        try:
            data = path.read_text(encoding="utf-8")
            (output / (name + ".txt")).write_text(data, encoding="utf-8")
            item.update(status="ok", file=name + ".txt")
        except OSError as exc:
            item.update(status="unavailable", error=str(exc))
        manifest["files"].append(item)
    manifest["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    with (output / "manifest.json").open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interface", required=True)
    parser.add_argument("--output", required=True, help="new directory; parent must exist")
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("--timeout must be in (0, 60]")
    try:
        manifest = collect(args.interface, args.output, args.timeout)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc) + "\n")
    unavailable = sum(x["status"] != "ok" for x in manifest["commands"] + manifest["files"])
    print(f"Saved inventory to {args.output}; {unavailable} unavailable/failed entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
