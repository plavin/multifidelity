#!/usr/bin/env bash
set -euo pipefail

base='../experiment-results/Jun-27-'
suffix='/trace'

mkdir -p results/Jun-28/

for i in {0..4}
do
    echo "Run $i"
    ./optimize ${base}${i}${suffix} > results/Jun-28/opt-${i}.out
done
