# Multifidelity Simulation

This repository contains the simulator used to write our MEMSYS 23 paper and my dissertation work. There are also a number of support scripts. 
## Prerequisites

You will need sst-core and sst-elements. Please use these specific commits.
- `sst-core`: [Link](https://github.com/sstsimulator/sst-core/commit/e70e231f097c24c5f9d6b4ec5d1b3cd217a5f6a4)
- `sst-elements`: [Link](https://github.com/plavin/sst-elements/commit/4d3e1758ab1381fe450852a670cb50df9f7bca5e)
## Basic operation

The main simulator script is `./simulate.py`. At a minimum, you must specify a config file (see [workloads](https://github.com/plavin/spec-utils/tree/main/workloads)), and an SST sdl file, which will be either `two-level.py` or `two-level-timingdram.py`. Thus, a simple invocation would look like this:
```
  ./simulate.py -c default-workload.py -s two-level.py
```

You will also want to specify a location of a Parrot, most likely between the L1 and the L2:
```
  ./simulate.py -c default-workload.py -s two-level.py -p l1
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
  -t, --trace           enable tracing
  -B, --backup          enable tracing
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


# Spec + Ariel

This README covers the workflow for woking with SPEC CPU and Ariel. 

1. Instal SPEC

  - SPEC is easy to install. Just copy over the whole directory to where you want it. Then run `./install`. It should just install into the directory it is in. This step might not even be necessary.

  - When working with SPEC, make sure you run `source shrc` to set up your environment. 

2. Create a SPEC config

  - Go into $SPEC/config and copy one of the existing config files. Edit the parts marked `EDIT`.

3. Choose your benchmarks

  - Create a file, such as `song-benchmarks.txt` with the names of the SPEC benchmarks you want to run.

4. Generate configs for Ariel

  - Use the command `./generate.py <config name> <benchmarks file>` to create a file with a dict of configs for Ariel. This dict has two fields: `cmd` and `directory`. The former is the command used to run the benchmark and the latter is the directory the command must be run from. The reason for the directory change is that some of the arguments to the program are relative paths to files. 
  - This can take 10 minutes on flubber8
  - Potential issues:
    - Check to see if there are more then 1 set of build directories for the benchmarks (e.g. are the directories ending in numbers greater than 0000, such as 0001, and 0002?) You may want to delete those and retry. 
      - `runcpu <config-name> -a clean all`
      - `runcpu <config-name> -a realclean all`
      - `runcpu <config-name> -a clobber all`
    - These commands may help as well
      - `rm -Rf $SPEC/benchspec/C*/*/run`
      - `rm -Rf $SPEC/benchspec/C*/*/build`
      - `rm -Rf $SPEC/benchspec/C*/*/exe`
    - You shouldn't need these anymore but I'm leaving this for reference.

5. Use `simulate.py`

  - For example, run `./simulate.py song_pattest_3.py spec_ariel_test.py 0` to run the first benchmark (index 0)

  
# Directories

1. `data-collection-scripts/`: Scripts used to invoke the `./simulation` command. These scripts should be copied to this directory to run properly.
2. `libftprjg/`: Stability detector library code
3. `libpd/`: Phase detector library code
4. `notebooks/`: Jupyter notebooks that generate plots. These should be moved to this directory to re-run them
5. `plots/`: Plots used in my dissertation and in the MEMSYS paper
