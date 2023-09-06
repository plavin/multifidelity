#!/usr/bin/env bash

OUTDIR=4ghz-study-4
TIME=30ms
BENCH=adi
mkdir -p $OUTDIR

./simulate.py -n 2 -s two-level.py -c polybench-workloads.py -b $BENCH --stop-at $TIME > $OUTDIR/no-parrot.out
./simulate.py -n 2 -s two-level.py -c polybench-workloads.py -b $BENCH --stop-at $TIME -p 'l1' -P '2.0GHz' > $OUTDIR/2ghz.out
./simulate.py -n 2 -s two-level.py -c polybench-workloads.py -b $BENCH --stop-at $TIME -p 'l1' -P '4.0GHz' > $OUTDIR/4ghz.out
