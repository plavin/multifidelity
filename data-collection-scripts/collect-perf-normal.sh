#!/usr/bin/env bash
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
./simulate.py -s two-level.py -c polybench-workloads.py -p l1 -n 5 -B -o polybench-medium-normal.pkl
