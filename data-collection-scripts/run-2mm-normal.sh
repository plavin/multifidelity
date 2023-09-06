#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

NAME=polybench-normal-2mm-subset-0
./simulate.py --stop-at=25ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1
mkdir -p parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-normal-2mm-subset-1
./simulate.py --stop-at=25ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1
mkdir -p parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-normal-2mm-full-0
./simulate.py --stop-at=25ms -s two-level.py -c polybench-workloads.py -t -b 2mm -o $NAME.pkl -p l1
mkdir -p parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-normal-2mm-full-1
./simulate.py --stop-at=25ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1
mkdir -p parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR
