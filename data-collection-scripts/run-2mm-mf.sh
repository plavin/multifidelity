#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

NAME=polybench-mf-2mm-subset-5
./simulate.py --stop-at=20ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1 -M
mkdir -p parrot-traces/$NAME
cp two-level-stats.csv parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-mf-2mm-subset-6
./simulate.py --stop-at=20ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1 -M
mkdir -p parrot-traces/$NAME
cp two-level-stats.csv parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-mf-2mm-subset-7
./simulate.py --stop-at=20ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1 -M
mkdir -p parrot-traces/$NAME
cp two-level-stats.csv parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

NAME=polybench-mf-2mm-subset-8
./simulate.py --stop-at=20ms -s two-level.py -c polybench-subset.py -t -b 2mm -o $NAME.pkl -p l1 -M
mkdir -p parrot-traces/$NAME
cp two-level-stats.csv parrot-traces/$NAME
mv $NAME.pkl parrot-traces/$NAME
cd parrot-traces
mv *.out $NAME
cd $SCRIPT_DIR

