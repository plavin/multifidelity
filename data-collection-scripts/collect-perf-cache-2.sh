#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
#./simulate.py -s two-level.py -c polybench-workloads.py -t -B -p l1
#!/bin/bash
for sz in 8KiB 16KiB 32KiB;
do
    for i in {1..3}
    do
        echo "--------" Run Normal $i $sz"--------"
        ./simulate.py -s two-level.py -c polybench-workloads.py -B -p l1 -z $sz
    done
done
