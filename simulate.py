#!/usr/bin/env python3

import sys
import os
from ariel_utils import parse_generate_py_configs as get_configs
import subprocess
from io import StringIO
import pandas as pd

STOP_AT = '500us'

def usage():
    print(f'Usage: {sys.argv[0]} <config dict file> <sdl file> [index,[index,...]] [parrot,[parrot,...]]')
    print('The first argument is the output of ./generate.py')
    print('Specify indices benchmarks to run. Specify `all` to run all benchmarks in config file.')

def build_profiling_string(profilers):
    if len(profilers) < 1:
        return ''
    result = '--enable-profiling=' #ClockStats:sst.profile.handler.clock.time.high_resolution(level=type)[clock]'
    for prof_name, prof_str in profilers.items():
        result += f'{prof_name}:{prof_str};'
    return result[:-1] # remove trailing semicolon

def parse_profiling(stdout, prof_names):
    lines = stdout.split('\n')
    df = {}
    for name in prof_names:
        found = False
        start = 0
        end = 0
        for i in range(len(lines)):
            if not found:
                if name not in lines[i]:
                    continue
                found = True
                start = i
            if '-------------------' in lines[i] or lines[i].strip() == '':
                end = i
                break
        df[name] = pd.read_csv(StringIO('\n'.join(lines[start+1:end])))
    return df

def parse_timing(stderr):
    # times are reported in seconds
    lines = stderr.split('\n')
    times = {}
    label = ['real', 'user', 'sys']
    for lab in label:
        found = False
        for l in lines:
            if lab == l[0:len(lab)]: # find line that starts with desired label
                times[lab] = float(l.split()[1])
                break
        if lab not in times.keys(): # check that the label was found at some point
            print(f'Error: Unable to parse `{lab}` time')
    return times

def parse_sim_time(stdout):
    lines = stdout.split('\n')
    for l in lines:
        if 'Simulation is complete' in l:
            return l.split()[5:7]
    print('FATAL ERROR: Simulation failed to complete. Please inspect output. TODO: Note location of output')
    sys.exit(1)

class SimStats():
    def __init__(self, command, prof_config):

        self.command = command
        self.prof_config = prof_config
        #print(f'PAT Command: {" ".join(command)}')
        #print(f'PAT Dir: {os.getcwd()}')
        subp = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', check=True)

        self.stdout = subp.stdout
        self.stderr = subp.stderr
        self.sim_time = parse_sim_time(subp.stdout)
        self.profile  = parse_profiling(subp.stdout, prof_config.keys())
        self.times    = parse_timing(subp.stderr)

    def __repr__(self):
        s = ''

        # Simulated time
        s += f'Simulated time: {" ".join(self.sim_time)}\n\n'

        # Profiling data
        for name, df in self.profile.items():
            s += (f'Profiler: {name}\n')
            s += str(df)
            s += '\n'

        # Data from `time` command
        if len(self.times) > 0:
            s += '\nTiming (seconds)\n'
            for l, t in self.times.items():
                s += f' {l}:\t{t}\n'

        return s

if __name__ == "__main__":

    if len(sys.argv) < 4:
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
    if sys.argv[3] == 'all':
        index = all_indices
    else:
        index = [int(i) for i in sys.argv[3].split(',')]
        for i in index:
            if i not in [*range(0, len(configs))]:
                print(f'Error: Specified index `{i}` out of range `{all_indices[0]}-{all_indices[-1]}`')
                sys.exit(1)

    # Parrots
    parrot_levels = ''
    if len(sys.argv) > 4:
        parrot_levels = sys.argv[4]

    print(f'index: {index}')
    print(f'parrot_levels: {parrot_levels}')


    # Run specified simulations
    stats_dict = {
                  'ClockStats' : 'sst.profile.handler.clock.time.high_resolution(level=type)[clock]',
                  'EventStats' : 'sst.profile.handler.event.time.high_resolution(level=type)[event]'
                 }

    prof_str = build_profiling_string(stats_dict)

    for b in index:
        print(f'Simulating {b}')
        command = [
                  'time', '-p',
                   '/nethome/plavin3/sst/install/bin/sst',
                   '--stop-at', STOP_AT,
                   #'--exit-after=0:0:10',
                   prof_str,
                   sdl_filename, '--', f'{config_filename}:{list(configs.keys())[b]} {parrot_levels}',
                  ]
        print(command)
        st = SimStats(command, stats_dict)
        print(st)
        print('Simulation completed. Output is in run.out and run.err.')

print('Done.')
