#!/usr/bin/env bash
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
./simulate.py -s two-level.py -c polybench-subset.py -p l1 -n 6 -B -o polybench-subset-medium-normal-0.pkl
./simulate.py -s two-level.py -c polybench-subset.py -p l1 -n 6 -B -o polybench-subset-medium-normal-1.pkl
./simulate.py -s two-level.py -c polybench-subset.py -M -p l1 -n 6 -B -o polybench-subset-medium-mf-0.pkl
./simulate.py -s two-level.py -c polybench-subset.py -M -p l1 -n 6 -B -o polybench-subset-medium-mf-1.pkl
