#!/usr/bin/env bash
set -euo pipefail

base='../experiment-results/Jul-17-'
suffix='/trace'

mkdir -p results/spatter/

for i in {17..21}
do
    echo "Run $((i-17))"
    ./optimize ${base}${i}${suffix} > results/spatter/opt-$((i-17)).out
done
