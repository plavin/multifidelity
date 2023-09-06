#!/usr/bin/env bash
set -euo pipefail

base='../experiment-results/Jul-18-'
suffix='/trace'
out='results/spatter-2/'

mkdir -p $out

for i in {5..14}
do
    echo "Run $((i-5))"
    ./optimize ${base}${i}${suffix} > $out/opt-$((i-5)).out
done
