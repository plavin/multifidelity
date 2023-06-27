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
import SimulationArgs
from scipy.stats import sem
from dataclasses import dataclass, field
import pickle
from RunData import RunData
import tempfile
from Subsetter import subsetter
import shutil
from multiprocessing import Process, Queue, Pool, Manager

sys.path.insert(0, './python')
import SimulationUtilities as SimUtil

def custom_error_callback(error):
        print(f'Got error: {error}')

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
        self.mean = statistics.mean(times)/nu.ms # time stored in ms
        if len(times) > 1:
            self.sem = sem(times)/nu.ms
            self.sd = statistics.stdev(times)/nu.ms
        else:
            self.sem = 0
            self.sd = 0
    def __repr__(self):
        return f'{self.mean:.2f} (+/-{self.sd:.2f}) ms (sem {self.sem:.2f})'

class SummaryRate:
    def __init__(self, times, unit):
        self.unit = unit
        tt = times
        while(len(tt) > 2 and statistics.stdev(tt) > 0.01):
            tt = sorted(tt)[1:]

        self.mean = statistics.harmonic_mean(tt)
        if len(tt) > 1:
            self.sem = sem(tt)
            self.sd = statistics.stdev(tt)
        else:
            self.sem = 0
            self.sd = 0
    def __repr__(self):
        return f'{self.mean:.3f} (+/-{self.sd:.3f}) ({self.sem:.3f} sem) {self.unit}'

def parse_sim_time(stdout):
    lines = stdout.split('\n')
    for l in lines:
        if 'Simulation is complete' in l:
            tm = l.split()[5:7]
            if tm[1] == 'ms':
                return float(tm[0]) * nu.ms
            elif tm[1] == 'us':
                return float(tm[0]) * nu.us
            print(f'Error: Unrecognized time unit: {tm[1]}')
            sys.exit(1)
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

def parse_statsfile(parrot_levels, stats_file):
    df = pd.read_csv(stats_file, delimiter=', ', engine='python')
    res = {}
    for level in parrot_levels:
        res[level] = histogram(df[df['ComponentName'] == f'Parrot_{level}'])
    instr_count = list(df[(df['ComponentName']=='Ariel') & (df['StatisticName']=='instruction_count')]['Count.u64'])[0]
    cycles = list(df[(df['ComponentName']=='Ariel') & (df['StatisticName']=='cycles')]['Count.u64'])[0]
    return res, instr_count/cycles

class SimStats():
    def __init__(self, command, prof_config, parrot_levels, nruns, stats_file):

        self.command = command
        self.prof_config = prof_config
        self.parrot_levels = parrot_levels
        #print(f'PAT Command: {" ".join(command)}')
        #print(f'PAT Dir: {os.getcwd()}')
        subp = []
        self.latency = []
        self.ipc = []
        self.nruns = nruns
        for i in range(self.nruns):
            #print(f'{i+1}/{self.nruns}', end=' ')
            sys.stdout.flush()
            subp.append(subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', check=True))
            # TODO: do data aggregation for latency
            latency_hist, ipc = parse_statsfile(parrot_levels, stats_file)
            if len(parrot_levels) > 0:
                self.latency.append(latency_hist)
            self.ipc.append(ipc)
            ip_temp, ind = subsetter(self.ipc)
            if ip_temp is not None:
                self.ipc = ip_temp
                continue
                #TODO: NEED TO SUBSET other vars using `ind`
                #if i > 0 and statistics.stdev(sorted(self.ipc)[-2:]) < 0.01 :
                #    continue

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
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.precision', 3,
                              ):
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

def run_one(command, stats_dict, parrot_list, backup_dir, bb, return_queue, sim_args, stats_file):
    st = SimStats(command, stats_dict, parrot_list, sim_args.nruns, stats_file)
    if sim_args.backup:
        backup_file = backup_dir.joinpath(f'SimStats_{bb}.pkl')
        with open(backup_file, 'wb') as bf:
            pickle.dump(st, bf)
    return_queue.put((bb, st))
    return st

def run(sim_args, project_dir):

    if sim_args.backup and not sim_args.dry_run:
        backup_dir = project_dir.joinpath('backup')
        backup_dir.mkdir()

    trace_dir = None
    if sim_args.trace:
        trace_dir = project_dir.joinpath('trace')
        if not sim_args.dry_run:
            trace_dir.mkdir()

    stop_at = '100ms'
    if sim_args.stop_at is not None:
        stop_at = sim_args.stop_at

    # Run specified simulations
    stats_dict = {
                  'ClockStats' : 'sst.profile.handler.clock.time.high_resolution(level=type)[clock]',
                  'EventStats' : 'sst.profile.handler.event.time.high_resolution(level=type)[event]'
                 }

    stats_dir = project_dir.joinpath('stats')
    if not sim_args.dry_run:
        stats_dir.mkdir()
    prof_str = build_profiling_string(stats_dict)

    manager = Manager()
    return_queue = manager.Queue()

    st = {}
    pool = Pool()
    for bb in sim_args.benchmarks:
        print(f'Simulating [{bb}] [{sim_args.nruns} times] ')
        sys.stdout.flush()

        stats_file = stats_dir.joinpath(f'two-level-stats-{bb}.csv')

        sdl_args = [str(sim_args.config_file), str(bb)]
        sdl_args.append('-S')
        sdl_args.append(str(stats_file))
        if sim_args.parrot_levels != '':
            sdl_args.append('-p')
            sdl_args.append(str(sim_args.parrot_levels))
        if sim_args.parrot_freq != '':
            sdl_args.append('-P')
            sdl_args.append(str(sim_args.parrot_freq))
        if sim_args.multifidelity:
            sdl_args.append('-M')
        if sim_args.trace:
            sdl_args.append('-t')
            sdl_args.append(str(trace_dir.resolve()))
        if sim_args.rrfile:
            sdl_args.append('-r')
            sdl_args.append(str(sim_args.rrfile.resolve()))

        command = [
                  'time', '-p',
                   '/nethome/plavin3/sst/install/bin/sst',
                   '--stop-at', stop_at,
                   #'--exit-after=0:0:10',
                   prof_str,
                   str(sim_args.sdl), '--',
                   *sdl_args
                  ]
        #print(command)
        #print(' '.join(command))
        if sim_args.parrot_levels != '':
            parrot_list = sim_args.parrot_levels.split(',')
        else:
            parrot_list = []

        if (sim_args.dry_run):
            print(f"DRY RUN: {' '.join(command)}")
        else:
            pool.apply_async(run_one, args=(command, stats_dict, parrot_list, backup_dir, bb, return_queue, sim_args, stats_file), error_callback=custom_error_callback)
            #st[bb] = run_one(command, stats_dict, parrot_list, backup_dir, bb, return_queue, sim_args)

    pool.close()
    pool.join()

    while not return_queue.empty():
        val = return_queue.get()
        st[val[0]] = val[1]

    return (RunData(sim_args, stats_dict, prof_str, st))

if __name__ == "__main__":
    sim_args = SimulationArgs.parse(sys.argv)
    print(sim_args)

    # Only need this if we're going to save some info
    if sim_args.trace or sim_args.backup:
        project_dir = SimUtil.make_project_dir('experiment-results', dry_run=sim_args.dry_run)
        info_str = f'Experiment data will be stored in: {project_dir}'
        print(info_str)
        print('-'*len(info_str))
    else:
        project_dir = None

    # Store configuration info
    if not sim_args.dry_run and sim_args.backup:
        config_dir = project_dir.joinpath('config')
        config_dir.mkdir()
        simconfig_file = config_dir.joinpath('SimConfig.txt')
        with open(simconfig_file, 'w') as file:
            file.write(' '.join(sys.argv))
            file.write('\n')
            file.write(str(sim_args))
        #print(f'copy from {sim_args.config_file} to {project_dir.joinpath(sim_args.config_file)}')
        shutil.copy(str(sim_args.config_file), str(config_dir.joinpath(sim_args.config_file)))
        shutil.copy(str(sim_args.sdl), str(config_dir.joinpath(sim_args.sdl)))

    ret = run(sim_args, project_dir)
    if sim_args.dry_run:
        sys.exit(0)
    if sim_args.backup:
        backup_file = project_dir.joinpath('SimStats.pkl')
        with open(backup_file, 'wb') as file:
            pickle.dump(ret, file)

    # Just use -B from now on. And don't pint out the profiler, that's kind of annoying
    #if ret.sim_args.outfile is not None:
    #    with ret.sim_args.outfile.open('wb') as file:
    #        print(f'Dumping run data to {ret.sim_args.outfile}')
    #        pickle.dump(ret, file)
    #else:
    #    for key in ret.st:
    #        print(f'\n{key} ' + '-'*30)
    #        print(ret.st[key])
    print('Done')
