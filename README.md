# Multifidelity Simulation

This repository contains the simulator used to write our MEMSYS 23 paper and my dissertation work. There are also a number of support scripts. 
## Prerequisites

You will need sst-core and sst-elements. Please use these specific commits.
- `sst-core`: [Link](https://github.com/sstsimulator/sst-core/commit/e70e231f097c24c5f9d6b4ec5d1b3cd217a5f6a4)
- `sst-elements`: [Link](https://github.com/plavin/sst-elements/commit/4d3e1758ab1381fe450852a670cb50df9f7bca5e)
## Basic operation

Before you run a simulation, you need a binary to trace. This directory includes a simple matrix multiply program for testing purposes. Navigate to `matmul/` and run `make`. 

```
cd matmul
make
cd ..
```

The main simulator script is `./simulate.py`. At a minimum, you must specify a config file (see [workloads](https://github.com/plavin/spec-utils/tree/main/workloads)), and an SST sdl file, which will be either `two-level.py` or `two-level-timingdram.py`.
We will use an example config script that is stored with the matmul example.
Thus, a simple invocation would look like this:
```bash
./simulate.py -c matmul/mm-workload.py -s two-level.py
```

You will also want to specify a location of a Parrot, most likely between the L1 and the L2:
```bash
./simulate.py -c matmul/mm-workload.py -s two-level.py -p l1
```

Here is the rest of the usage information for the `./simulate.py` script:

```
$ ./simulate.py -h
usage: simulate.py [-h] -s SDL_FILE -c CONFIG_FILE [-b BENCHMARKS]
                   [-p PARROT_LEVELS] [-n NRUNS] [-N NCORES] [-t] [-B] [-M]
                   [-o OUTFILE] [-r RRFILE] [--stop-at STOP_AT] [--dry]
                   [-P PARROT_FREQ] [-z L1_CACHE]

optional arguments:
  -h, --help            show this help message and exit
  -s SDL_FILE, --sdl-file SDL_FILE
                        an SST SDL file
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        file containing dict of benchmark specifications
  -b BENCHMARKS, --benchmarks BENCHMARKS
                        comma separated list of benchmarks from the config
  -p PARROT_LEVELS, --parrot-levels PARROT_LEVELS
                        comma separated list of cache levels to enable the
                        Parrot on
  -n NRUNS, --nruns NRUNS
                        number of times to repeat each benchmark
  -N NCORES, --ncores NCORES
                        number of cores
  -t, --trace           enable tracing of Parrot
  -B, --backup          enable backup of SimStats
  -M, --multifidelity   enable multifidelity
  -o OUTFILE, --outfile OUTFILE
                        file to print to
  -r RRFILE, --rrfile RRFILE
                        file to read representative regions from
  --stop-at STOP_AT     how long to run simulations for
  --dry                 only print the sst command
  -P PARROT_FREQ, --parrot-freq PARROT_FREQ
                        speed of parrot component
  -z L1_CACHE, --l1-cache L1_CACHE
                        size of l1 cache
```

Example usage of many of these options will be found in the `data-collection-scripts/` directory.

## Important options

### Dry runs

You may want to run the SST sdl (`two-level.py`) directly, perhaps because the program is crashing and `simulate.py` is eating the output. The sdl has many of the same arguments as `./simulate.py`, which you can see with the following command:
```
sst two-level.py -- -h
```

_However_, it is easier to have `./simulate.py` give you the arguments it was using as a starting point. You can use the `--dry` option which should avoid making any output directories, even if `-B`, `-t`, or `-o` were specified.
```bash
./simulate.py -c matmul/mm-workload.py -s two-level.py -p l1 --dry
```

Dry runs are also a great way to see where stuff will be stored when you run with `-t` enabled. 

### Stop At

You may want to stop your simulations early if they take too long. Use the `--stop-at` option, which accepts anything that sst recognizes. For instance:
```
  ./simulate.py --stop-at=100ms [other options]
```
  
# Directories

1. `data-collection-scripts/`: Scripts used to invoke the `./simulation` command. These scripts should be copied to this directory to run properly.
2. `libftprjg/`: Stability detector library code
3. `libpd/`: Phase detector library code
4. `notebooks/`: Jupyter notebooks that generate plots. These should be moved to this directory to re-run them
5. `notebooks/dissertation-figures` and `notesbooks/plots`: Figures used in the papers
6. `plots/`: Plots used in my dissertation and in the MEMSYS paper
7. `spec-utils/`: Utilities to help you run SPEC in Ariel
