#!/usr/bin/env python3

import sys
import pathlib
import argparse
from dataclasses import dataclass, field
from ariel_utils import parse_generate_py_configs as get_configs

@dataclass(frozen=True)
class SimulationArgs:
    config: dict          = field(default_factory=dict)
    config_file: str      = None
    benchmarks: list      = field(default_factory=list)
    parrot_levels: str    = ''
    nruns: int            = 1
    ncores: int           = 1
    trace: bool           = False
    backup: bool          = False
    multifidelity: bool   = False
    dry_run: bool         = False
    stop_at: str          = '100ms'
    parrot_freq: str      = '2.0GHz'
    rrfile: pathlib.Path  = None
    sdl: pathlib.Path     = None
    outfile: pathlib.Path = None
    l1_cache: str        = '4KiB'

    def __str__(self):
        if self.outfile is None:
            outfile_string = 'None'
        s = 'Simulation Configuration:\n'
        s += f' config:        {len(self.config)} configs ({self.config_file})\n'

        if (len(self.benchmarks) > 5):
            s += f' benchmarks:    {len(self.benchmarks)} benchmarks\n'
        else:
            s += f' benchmarks:    {self.benchmarks}\n'

        s += f' parrot_levels: {self.parrot_levels}\n'
        s += f' nruns:         {self.nruns}\n'
        s += f' ncores:        {self.ncores}\n'
        s += f' trace:         {self.trace}\n'
        s += f' backup:        {self.backup}\n'
        s += f' multifidelity: {self.multifidelity}\n'
        s += f' stop_at:       {self.stop_at}\n'
        s += f' l1_cache:      {self.l1_cache}\n'
        s += f' dry_run:       {self.dry_run}\n'
        s += f' sdl:           {self.sdl}\n'
        s += f' parrot_freq:   {self.parrot_freq}\n'
        s += f' rrfile:        {self.rrfile}\n'
        s += f' outfile:       {self.outfile}'

        return s


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sdl-file', help='an SST SDL file', type=str, required=True)
    parser.add_argument('-c', '--config-file', help='file containing dict of benchmark specifications', type=str, required=True)
    parser.add_argument('-b', '--benchmarks', help='comma separated list of benchmarks from the config', type=str, required=False, default='all')
    parser.add_argument('-p', '--parrot-levels', help='comma separated list of cache levels to enable the Parrot on', type=str, required=False, default='')
    parser.add_argument('-n', '--nruns', help='number of times to repeat each benchmark', type=int, required=False, default=1)
    parser.add_argument('-N', '--ncores', help='number of cores', type=int, required=False, default=1)
    parser.add_argument('-t', '--trace', help='enable tracing', required=False, action="store_true")
    parser.add_argument('-B', '--backup', help='enable tracing', required=False, action="store_true")
    parser.add_argument('-M', '--multifidelity', help='enable multifidelity', required=False, action="store_true")
    parser.add_argument('-o', '--outfile', help='file to print to', type=str, required=False, default=None)
    parser.add_argument('-r', '--rrfile', help='file to read representative regions from', type=str, required=False, default=None)
    parser.add_argument('--stop-at', help= 'how long to run simulations for', type=str, required=False, dest='stop_at', default='100ms')
    parser.add_argument('--dry', help='only print the sst command', required=False, action="store_true")
    parser.add_argument('-P', '--parrot-freq', help='speed of parrot component', type=str, required=False, default='2.0GHz')
    parser.add_argument('-z', '--l1-cache', help='size of l1 cache', type=str, required=False, default='4KiB')

    args = parser.parse_args(argv[1:])

    if not pathlib.Path(args.config_file).is_file():
        raise FileNotFoundError(f'Config file ({args.config_file}) was not found')

    sdl_path = pathlib.Path(args.sdl_file)
    if not sdl_path.is_file():
        raise FileNotFoundError(f'SDL File ({args.sdl_file}) was not found')

    outfile_path = None
    if args.outfile is not None:
        outfile_path = pathlib.Path(args.outfile)

    rr_path = None
    if args.rrfile is not None:
        rr_path = pathlib.Path(args.rrfile)

        if not rr_path.is_file():
            raise FileNotFoundError(f'RR File ({args.rrfile}) was not found')

    configs = get_configs(args.config_file)
    if len(configs) < 1:
        raise Error('No configs parsed')

    benchlist = args.benchmarks.split(',')
    benchlist = list(set(benchlist))
    if 'all' not in benchlist:
        for bb in benchlist:
            if bb not in configs.keys():
                raise ValueError(f'benchmark ({bb}) not found in config ({args.config_file})')
    else:
        benchlist = [*configs.keys()]

    return SimulationArgs(config = get_configs(args.config_file),
                          config_file = args.config_file,
                          benchmarks = benchlist,
                          parrot_levels = args.parrot_levels,
                          nruns = args.nruns,
                          ncores = args.ncores,
                          trace = args.trace,
                          backup = args.backup,
                          multifidelity = args.multifidelity,
                          dry_run = args.dry,
                          parrot_freq = args.parrot_freq,
                          l1_cache = args.l1_cache,
                          sdl = sdl_path,
                          outfile = outfile_path,
                          rrfile = rr_path,
                          stop_at = args.stop_at)

if __name__ == '__main__':
    print(parse(sys.argv))
