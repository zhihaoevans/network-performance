#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .local
make -C examples/dpdk-mbuf
python3 scripts/dpdk_lab.py hello > .local/dpdk-hello.log 2>&1
python3 scripts/dpdk_lab.py mbuf > .local/dpdk-mbuf.log 2>&1
python3 scripts/dpdk_lab.py null --smoke > .local/dpdk-null.log 2>&1
python3 scripts/check_docs.py
printf '%s\n' 'DPDK functional self-check passed. See .local/dpdk-*.log and dpdk/codespaces.md.'
