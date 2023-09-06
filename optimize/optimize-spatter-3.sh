#!/usr/bin/env bash
set -euo pipefail

out='results/spatter-4/'

mkdir -p $out

echo 1
./optimize ../experiment-results/Jul-23-13/trace > $out/opt-0.out
echo 2
./optimize ../experiment-results/Jul-23-14/trace > $out/opt-1.out
echo 3
./optimize ../experiment-results/Jul-23-15/trace > $out/opt-2.out
echo 4
./optimize ../experiment-results/Jul-23-16/trace > $out/opt-3.out
echo 5
./optimize ../experiment-results/Jul-24-0/trace > $out/opt-4.out
