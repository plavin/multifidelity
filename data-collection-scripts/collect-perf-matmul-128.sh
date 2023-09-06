#!/usr/bin/env bash
set -euo pipefail
# -t: generate traces
# -M: multifidelity runs
# -p: Parrot above l1
# NOTE: You need the parrot to trace, but we should do another timing run without it
#./simulate.py -s two-level.py -c polybench-workloads.py -t -B -p l1

#for i in {1..5}
#do
#    echo "--------" Run Normal $i "--------"
#    ./simulate.py -s two-level.py -c matmul-workloads.py -B -t -p l1
#done
#

for i in {1..1}
do
    echo "--------" Run Norm $i "--------"
    ./simulate.py -s two-level.py -c matmul-128-workloads.py -p l1 --stop-at=5ms -N 4
done

curl -d "Simulation Complete" ntfy.sh/sst_sim_complete
