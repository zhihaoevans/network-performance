#!/usr/bin/env python3
"""Summarize explicit receiver totals from completed, unidirectional iperf3 -J files."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys


def numeric(obj, key, required=False):
    value = obj.get(key)
    if value is None and not required:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"invalid/missing numeric field: {key}")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"invalid numeric value: {key}")
    return value


def summarize(data, source=""):
    if not isinstance(data, dict):
        raise ValueError("expected one JSON object, not a stream/array")
    if data.get("error"):
        raise ValueError("iperf error: " + str(data["error"]))
    start, end = data.get("start", {}), data.get("end", {})
    if not isinstance(start, dict) or not isinstance(end, dict):
        raise ValueError("missing/invalid start or end")
    config = start.get("test_start", {})
    if not isinstance(config, dict):
        raise ValueError("missing test_start")
    if config.get("bidir") or config.get("bidirectional") or any("bidir" in k for k in end):
        raise ValueError("bidirectional JSON is not supported; split the directions")
    protocol = config.get("protocol")
    if protocol not in ("TCP", "UDP"):
        raise ValueError("only explicit TCP/UDP test_start.protocol is supported")
    receiver = end.get("sum_received")
    selected = "end.sum_received"
    if receiver is None and protocol == "UDP":
        candidate = end.get("sum")
        if isinstance(candidate, dict) and candidate.get("sender") is False:
            receiver, selected = candidate, "end.sum"
    if not isinstance(receiver, dict) or receiver.get("sender") is True:
        raise ValueError("no unambiguous receiver total; retain and inspect raw JSON")
    bps = numeric(receiver, "bits_per_second", required=True)
    seconds = numeric(receiver, "seconds", required=True)
    if seconds == 0:
        raise ValueError("receiver interval must be positive")
    sender = end.get("sum_sent")
    retransmits = numeric(sender, "retransmits") if protocol == "TCP" and isinstance(sender, dict) else None
    lost_percent = numeric(receiver, "lost_percent") if protocol == "UDP" else None
    if lost_percent is not None and lost_percent > 100:
        raise ValueError("lost_percent exceeds 100")
    return {
        "file": source, "protocol": protocol,
        "reverse": bool(config.get("reverse", False)),
        "parallel_streams": numeric(config, "num_streams"),
        "receiver_source": selected, "receiver_seconds": seconds,
        "receiver_bytes": numeric(receiver, "bytes"), "receiver_mbps": bps / 1_000_000,
        "sender_retransmits": retransmits,
        "receiver_packets": numeric(receiver, "packets") if protocol == "UDP" else None,
        "receiver_lost_packets": numeric(receiver, "lost_packets") if protocol == "UDP" else None,
        "receiver_lost_percent": lost_percent,
        "receiver_jitter_ms": numeric(receiver, "jitter_ms") if protocol == "UDP" else None,
    }


def reject_constant(value):
    raise ValueError("non-standard JSON number: " + value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    args = parser.parse_args()
    rows = []
    for path in args.files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)
            rows.append(summarize(data, str(path)))
        except (OSError, ValueError, TypeError) as exc:
            parser.exit(2, f"{path}: {exc}\n")
    if args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
