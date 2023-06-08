#!/usr/bin/env bash
#set -euo pipefail

bench='syr2k covariance floyd-warshall jacobi-2d'
nruns=1
nrepeats=2
stopat="10ms"

echo "bench: "$bench
echo "nruns: "$nruns
echo "nrepeats: "$nrepeats
echo "stopat: "$stopat

for be in $bench;
do
    echo "=========" $be
    echo 'Normal'
    for i in `seq 1 $nrepeats`;
    do
        echo -n "$i "
        ./simulate.py -b $be -c polybench-workloads.py -s two-level.py --stop-at=$stopat  -n$nruns | grep ipc
    done

    echo 'Multifidelity'
    for i in `seq 1 $nrepeats`;
    do
        echo -n $i
        ./simulate.py -b $be -c polybench-workloads.py -s two-level.py --stop-at=$stopat  -n$nruns -M | grep ipc
    done
done
