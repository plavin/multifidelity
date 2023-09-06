#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
NAME=polybench-mf-2mm
./simulate.py -s two-level.py -c polybench-workloads.py -t -b 2mm -o $NAME.pkl -p l1 -M
mkdir -p parrot-traces/$NAME
cp $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME

