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

for sz in 8KiB 16KiB 32KiB 64KiB;
do
    for i in {1..3}
    do
        echo "--------" Run Norm $i size=$sz "--------"
        ./simulate.py -s two-level.py -c matmul-128-workloads.py -p l1 -B --stop-at=25ms -z $sz -t
    done
    #for i in {1..3}
    #do
    #    echo "--------" Run MF $i size=$sz "--------"
    #    ./simulate.py -s two-level.py -c matmul-128-workloads.py -p l1 -B --stop-at=25ms -z $sz -M
    #done
done

for threads in 2 4 8;
do
    for i in {1..3}
    do
        echo "--------" Run Norm $i threads=$threads "--------"
        ./simulate.py -s two-level.py -c matmul-128-workloads.py -p l1 -B --stop-at=25ms -N $threads -t -z 32KiB
    done
    #for i in {1..3}
    #do
    #    echo "--------" Run MF $i threads=$threads "--------"
    #    ./simulate.py -s two-level.py -c matmul-128-workloads.py -p l1 -B --stop-at=25ms -N $threads -M
    #done
done

#curl -d "Simulation Complete" ntfy.sh/sst_sim_complete
