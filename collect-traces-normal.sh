#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
./simulate.py -s two-level.py -c polybench-workloads.py -t -B -o polybench-normal-jun14.pkl -p l1
mkdir -p parrot-traces/polybench-normal-jun14
cp polybench-normal-jun14.pkl parrot-traces/polybench-normal-jun14/
cd parrot-traces
mv *.out polybench-normal-jun14

