#!/usr/bin/env bash
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
./simulate.py -s two-level.py -c polybench-workloads.py -t -B -o polybench-good-normal.pkl -p l1
