#!/usr/bin/env bash
set -euo pipefail

base='../experiment-results/Jul-14-'
suffix='/trace'

mkdir -p results/matmul/

for i in {0..4}
do
    echo "Run $i"
    ./optimize ${base}${i}${suffix} > results/matmul/opt-${i}.out
done
