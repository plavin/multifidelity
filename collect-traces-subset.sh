#!/usr/bin/env bash
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1

./simulate.py -s two-level.py -c polybench-subset.py -t -p l1 -B -o polybench-subset-normal.pkl
cd parrot-traces
mkdir -p polybench-subset-normal-jun14
mv *.out polybench-subset-normal-jun14/
cd ..
cp polybench-subset-normal.pkl parrot-traces/polybench-subset-normal-jun14

./simulate.py -s two-level.py -c polybench-subset.py -t -M -p l1 -B -o polybench-subset-mf.pkl
cd parrot-traces
mkdir -p polybench-subset-mf-jun14
mv *.out polybench-subset-mf-jun14/
cd ..
cp polybench-subset-mf.pkl parrot-traces/polybench-subset-mf-jun14
# ./simulate.py -s two-level.py -c polybench-subset.py -b 2mm -t -M -p l1 -B -o polybench-subset-mf-nanofix-2mmonly.pkl
