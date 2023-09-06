#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
#./simulate.py -s two-level.py -c polybench-workloads.py -t -B -p l1
#!/bin/bash
for sz in 1KiB 2KiB;
do
    for i in {1..5}
    do
        echo "--------" Run Normal $i $sz"--------"
        ./simulate.py -s two-level.py -c polybench-workloads.py -B -p l1 -z $sz
    done
done

for sz in 1KiB 2Kib;
do
    for i in {1..5}
    do
        echo "--------" Run MF $i $sz"--------"
        ./simulate.py -s two-level.py -c polybench-workloads.py -B -p l1 -M -z $sz
    done
done


