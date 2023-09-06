#!/usr/bin/env bash
set -euo pipefail

base='../experiment-results/Jul-06-'
suffix='/trace'

mkdir -p results/Jul-06-SPEC/

for i in {0..4}
do
    echo "Run $i"
    ./optimize ${base}${i}${suffix} > results/Jul-06-SPEC/opt-${i}.out
done
