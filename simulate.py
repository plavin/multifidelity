#!/usr/bin/env python3

import sys
import os
from ariel_utils import parse_generate_py_configs as get_configs
import subprocess
from io import StringIO
import pandas as pd
import numpy as np
import statistics
import numericalunits as nu

STOP_AT = '100ms'
NRUNS = 2

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

def parse_profiling_list(stdout_list, prof_names):
    # TODO this function should aggregate this list
    ret = []
    for stdout in stdout_list:
        ret.append(parse_profiling(stdout, prof_names))
    return ret

class RealTime:
    def __init__(self, timings):
        self.real = SimTime([float(a['real'])*nu.s for a in timings])
        self.user = SimTime([float(a['user'])*nu.s for a in timings])
        self.sys = SimTime([float(a['sys'])*nu.s for a in timings])
    def __repr__(self):
        ret = 'Wallclock Time:\n  '
        ret = ret + 'Real: ' + str(self.real) + '\n  '
        ret = ret + 'User: ' + str(self.user) + '\n  '
        ret = ret + 'Sys:  ' + str(self.sys)
        return ret

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

def parse_timing_list(stderr_list):
    # TODO this function should aggregate this list
    ret = []
    for stderr in stderr_list:
        ret.append(parse_timing(stderr))

    return RealTime(ret)

class SimTime:
    def __init__(self, times):
        self.mean = statistics.mean(times)
        if len(times) > 1:
            self.stdev = statistics.stdev(times)
        else:
            self.stdev = 0
    def __repr__(self):
        return f'{self.mean/nu.ms:.2f} (+/-{self.stdev/nu.ms:.2f}) ms'

class SummaryRate:
    def __init__(self, times, unit):
        self.mean = statistics.harmonic_mean(times)
        if len(times) > 1:
            self.stdev = statistics.stdev(times)
        else:
            self.stdev = 0
        self.unit = unit
    def __repr__(self):
        return f'{self.mean:.3f} (+/-{self.stdev:.3f}) {self.unit}'

def parse_sim_time(stdout):
    lines = stdout.split('\n')
    for l in lines:
        if 'Simulation is complete' in l:
            tm = l.split()[5:7]
            if tm[1] != 'ms':
                print(f'Error: Unrecognized time unit: {tm[1]}')
                sys.exit(1)
            return float(tm[0]) * nu.ms
    print('FATAL ERROR: Simulation failed to complete. Please inspect output. TODO: Note location of output')
    sys.exit(1)

def parse_sim_time_list(stdout_list):
    times = []
    for stdout in stdout_list:
        times.append(parse_sim_time(stdout))
    return SimTime(times)

class histogram:
    def __init__(self, df) -> None:
        self.df = df
        self.MinValue = list(df['BinsMinValue.u64'])[0]
        self.MaxValue = list(df['BinsMaxValue.u64'])[0]
        self.BinWidth = list(df['BinWidth.u32'])[0]
        self.TotalNumBins = list(df['TotalNumBins.u32'])[0]
        self.OOBMin = list(df['NumOutOfBounds-MinValue.u64'])[0]
        self.OOBMax = list(df['NumOutOfBounds-MaxValue.u64'])[0]


        self.data = []
        for i in range(self.TotalNumBins):
            self.data.append(list(df[f'Bin{i}:{self.MinValue + i*self.BinWidth}-{self.MinValue + (i+1)*self.BinWidth-1}.u64'])[0])

    def __repr__(self) -> str:
        ret = 'Histogram: '
        return str(self.data)

def parse_statsfile(parrot_levels):
    df = pd.read_csv('two-level-stats.csv', delimiter=', ', engine='python')
    res = {}
    for level in parrot_levels:
        res[level] = histogram(df[df['ComponentName'] == f'Parrot_{level}'])
    instr_count = list(df[(df['ComponentName']=='Ariel') & (df['StatisticName']=='instruction_count')]['Count.u64'])[0]
    cycles = list(df[(df['ComponentName']=='Ariel') & (df['StatisticName']=='cycles')]['Count.u64'])[0]
    return res, instr_count/cycles

class SimStats():
    def __init__(self, command, prof_config, parrot_levels):

        self.command = command
        self.prof_config = prof_config
        self.parrot_levels = parrot_levels
        #print(f'PAT Command: {" ".join(command)}')
        #print(f'PAT Dir: {os.getcwd()}')
        subp = []
        self.latency = []
        self.ipc = []
        for i in range(NRUNS):
            print(f'{i+1}/{NRUNS}', end=' ')
            sys.stdout.flush()
            subp.append(subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', check=True))
            # TODO: do data aggregation for latency
            latency_hist, ipc = parse_statsfile(parrot_levels)
            self.latency.append(latency_hist)
            self.ipc.append(ipc)
        print()

        #self.stdout = subp.stdout
        #self.stderr = subp.stderr
        self.sim_time = parse_sim_time_list([sp.stdout for sp in subp])
        self.profile  = parse_profiling_list([sp.stdout for sp in subp], prof_config.keys())
        self.times    = parse_timing_list([sp.stderr for sp in subp])
        self.IPC      = SummaryRate(self.ipc, 'ipc')

    def __repr__(self):
        s = ''

        # Profiling data
        # TODO: Add this back in
        for name, df in self.profile[0].items():
            s += (f'Profiler: {name}\n')
            s += str(df)
            s += '\n'

        # Simulated time
        s += f'Simulated time:\n  {self.sim_time}\n'


        # Data from `time` command
        s += str(self.times)
        s += '\n'

        s += 'Simulated IPC:\n  '
        s += str(self.IPC)

        return s

def run(argv):
    print(argv)
    if len(argv) < 4:
        usage()
        sys.exit(1)

    # Check that config file exists
    config_filename = argv[1]
    if (not os.path.exists(config_filename)):
        print(f'Can\'t find config file: {config_filename}')
        sys.exit(1)

    # Check that sdl file exists
    sdl_filename = argv[2]
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
    if argv[3] == 'all':
        index = all_indices
    else:
        index = [int(i) for i in argv[3].split(',')]
        for i in index:
            if i not in [*range(0, len(configs))]:
                print(f'Error: Specified index `{i}` out of range `{all_indices[0]}-{all_indices[-1]}`')
                sys.exit(1)

    # Parrots
    parrot_levels = ''
    if len(argv) > 4:
        parrot_levels = argv[4]

    print(f'index: {index}')
    print(f'parrot_levels: {parrot_levels}')


    # Run specified simulations
    stats_dict = {
                  'ClockStats' : 'sst.profile.handler.clock.time.high_resolution(level=type)[clock]',
                  'EventStats' : 'sst.profile.handler.event.time.high_resolution(level=type)[event]'
                 }

    prof_str = build_profiling_string(stats_dict)

    st = {}
    for b in index:
        print(f'Simulating {b} [{list(configs.keys())[b]}]')
        command = [
                  'time', '-p',
                   '/nethome/plavin3/sst/install/bin/sst',
                   '--stop-at', STOP_AT,
                   #'--exit-after=0:0:10',
                   prof_str,
                   sdl_filename, '--', f'{config_filename}:{list(configs.keys())[b]} {parrot_levels}',
                  ]
        #print(command)
        st[list(configs.keys())[b]] = SimStats(command, stats_dict, parrot_levels.split(','))
    return (st)

if __name__ == "__main__":
    st = run(sys.argv)
    for key in st:
        print(f'\n{key} ' + '-'*30)
        print(st[key])
    print('Done')
