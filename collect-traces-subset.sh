#!/usr/bin/env bash
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
#./simulate.py -s two-level.py -c polybench-subset.py -t -p l1 -B -o polybench-subset-normal.pkl
#./simulate.py -s two-level.py -c polybench-subset.py -t -M -p l1 -B -o polybench-subset-mf.pkl
./simulate.py -s two-level.py -c polybench-subset.py -b 2mm -t -M -p l1 -B -o polybench-subset-mf-newparams-2mmonly.pkl
