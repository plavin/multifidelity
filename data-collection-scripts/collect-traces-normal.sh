#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
#./simulate.py -s two-level.py -c polybench-workloads.py -t -B -p l1
#!/bin/bash
for i in {1..5}
do
    echo "--------" Run $i "--------"
    ./simulate.py -s two-level.py -c polybench-workloads.py -t -B -p l1
done

