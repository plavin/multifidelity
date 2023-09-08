#!/usr/bin/env python3

# Automating steps from here: https://www.spec.org/cpu2017/Docs/runcpu-avoidance.html

import pprint
import sys
import os
import re
import subprocess
from os.path import exists

def print_separator():
    print('# -----------------------------------------------')
def print_prefix(string, end='\n'):
    print('# ' + string, end=end)

# Parse arguments
if (len(sys.argv) < 3):
    print_prefix(f'Usage: {sys.argv[0]} <config name> <benchmark file>')
    sys.exit(1)
config=sys.argv[1]
benchmark_file=sys.argv[2]

# Find SPEC installation
try:
    spechome = os.environ['SPEC']
except:
    print_prefix("Unable to find SPEC location in evironment")
    sys.exit(1)
if (spechome == ""):
    print_prefix("Couldn't find spec location")
    sys.exit(1)

# Check that config file exists
config_file = os.path.join(spechome, 'config', config) + ".cfg"
if (not exists(config_file)):
    print_prefix(f"Can't find benchmark file: {config_file}")
    sys.exit(1)

# Check that benchmark file exists
if (not exists(benchmark_file)):
    print_prefix(f"Can't find benchmark file: {benchmark_file}")
    sys.exit(1)

# Output configuration information
print_separator()
print_prefix(f'SPEC home is:\t\t{spechome}')
print_prefix(f'Config file:\t\t$SPEC/config/{config}.cfg')
print_prefix(f'Benchmark file:\t{benchmark_file}')
print_separator()

# Parse benchmark file
benchmark = []
with open(benchmark_file, "r") as benchfile:
    lines = benchfile.readlines()
    for line in lines:
        bench = "".join(line.split())
        if bench == "" or bench[0] == "#":
            continue
        benchmark.append(bench)

if (len(benchmark) == 0):
    print("No benchmarks specified.")
    sys.exit(1)

# Output benchmark information
benchmark_string = benchmark[0]
for bench in benchmark[1:]:
    benchmark_string = benchmark_string + " "  + bench
print_prefix(f'Generating configs for: {benchmark_string}')
print_separator()

# Get test label from config file
with open(config_file, 'r') as cf:
    for line in cf.readlines():
        x = re.findall("^\%define label", line)
        if x:
            test_label = line.split()[2]
            break

# Execute fake run to set up directories
step1 = {}
configs = {}
print_prefix('Step 1: Execute fake run to set up directories')
for bench in benchmark:
    print_prefix(f'{bench}: ', end='')
    # Make sure binaries are built
    os.popen("runcpu --action runsetup --loose --size test --tune base --config {} {}".format(config, bench)).read()
    # Need output for next step
    out = os.popen("runcpu --fake --loose --size test --tune base --config {} {}".format(config, bench)).read()

    # Make sure run completed successfully
    regex = "Success:.*" + re.escape(bench)
    if not (re.search(regex, out)):
        print('failure - failed to complete test run successfully')
        step1[bench] = False

    # Make sure we can find directory
    found_dir = False
    for line in out.split('\n'):
        x = re.findall("^cd ", line)
        if x:
            configs[bench] = {'directory':line.split()[1]}
            found_dir = True
            break

    if not found_dir:
        print('failure - failed to find run directory')
        step1[bench] = False
    else:
        print('success')
        step1[bench] = True


# Check that step1 passed for all benchmarks
if (not all(step1)):
    print(f'Error: Step 1 failed to complete for some benchmarks')
    sys.exit(1)

step2 = {}

print_separator()
print_prefix('Step 2: Parse logs from step 1 to determine how to invoke benchmark')

for bench in benchmark:
    print(f'# {bench}: ', end='')
    bindir = configs[bench]['directory']
    try:
        os.chdir(bindir)
    except:
        step2[bench] = False
        print('failure - unable to change to benchmark directory')
        continue


    # run specinvoke
    out = os.popen("specinvoke -n").read()

    found = False
    for line in out.splitlines():
        x = re.findall("^#", line)
        if x:
            continue
        x = re.findall("^specinvoke", line)
        if x:
            continue
        configs[bench]['cmd'] = line

    step2[bench] = True
    print('success')

# Check that step2 passed for all benchmarks
if (not all(step2)):
    print(f'Error: Step 2 failed to complete for some benchmarks')

print_separator()
print_prefix('Done. Printing configs. Call eval() on the output of this program to get the configs.')
print_separator()
print()
pp = pprint.PrettyPrinter(indent=2, compact=True)
pp.pprint(configs)


