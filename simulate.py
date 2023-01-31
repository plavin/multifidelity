#!/usr/bin/env python3

import sys
import os
from ariel_utils import parse_generate_py_configs as get_configs
import subprocess

def usage():
    print(f'Usage: {sys.argv[0]} <config dict file> <sdl file> [index [index ...]]')
    print('The first argument is the output of ./generate.py')
    print('Specify indices benchmarks to run. Leaving blank will run all benchmarks in config file.')

if __name__ == "__main__":

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    # Check that config file exists
    config_filename = sys.argv[1]
    if (not os.path.exists(config_filename)):
        print(f'Can\'t find config file: {config_filename}')
        sys.exit(1)

    # Check that sdl file exists
    sdl_filename = sys.argv[2]
    if (not os.path.exists(sdl_filename)):
        print(f'Can\'t find sdl file: {sdl_filename}')
        sys.exit(1)

    # Parse configs
    configs = get_configs(config_filename)
    if len(configs) < 1:
        print(f'No configs parsed.')
        sys.exit(1)

    # Parse which configs to run
    index = []
    all_indices = [*range(0, len(configs))]
    if len(sys.argv) == 3:
        index = all_indices
    else:
        for i in range(3, len(sys.argv)):
            try:
                index.append(int(sys.argv[i]))
            except:
                print(f'Error: Unable to parse `{sys.argv[i]}` as int')
                sys.exit(1)

        for i in index:
            if i not in [*range(0, len(configs))]:
                print(f'Error: Specified index `{i}` out of range `{all_indices[0]}-{all_indices[-1]}`')
                sys.exit(1)


    # Run specified simulations
    for b in index:
        print(f'Simulating {b}')
        command = ['/nethome/plavin3/sst/install/bin/sst', '--stop-at', '10ms', sdl_filename,
        #           '--enable-profiling=events:sst.profile.handler.event.time.high_resolution(level=type)[event]',
                   '--', config_filename, list(configs.keys())[b]]
        print(' '.join(command))
        subprocess.run(command)
        #print(['/nethome/plavin3/sst/install/bin/sst', '--stop-at', '10ms', sdl_filename,
        #                '--', config_filename, list(configs.keys())[b]])



print('Done.')
