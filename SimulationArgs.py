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
    parrot_levels: list   = field(default_factory=list)
    nruns: int            = 1
    trace: bool           = False
    sdl: pathlib.Path     = None
    outfile: pathlib.Path = None

    def __str__(self):
        if self.outfile is None:
            outfile_string = 'None'
        s = ''
        s += f'config:        {len(self.config)} configs ({self.config_file})\n'
        s += f'benchmarks:    {self.benchmarks}\n'
        s += f'parrot_levels: {self.parrot_levels}\n'
        s += f'nruns:         {self.nruns}\n'
        s += f'trace:         {self.trace}\n'
        s += f'sdl:           {self.sdl}\n'
        s += f'outfile:       {self.outfile}'

        return s


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sdl-file', help='an SST SDL file', type=str, required=True)
    parser.add_argument('-c', '--config-file', help='file containing dict of benchmark specifications', type=str, required=True)
    parser.add_argument('-b', '--benchmarks', help='comma separated list of benchmarks from the config', type=str, required=False, default='all')
    parser.add_argument('-p', '--parrot-levels', help='comma separated list of cache levels to enable the Parrot on', type=str, required=False, default=[])
    parser.add_argument('-n', '--nruns', help='number of times to repeat each benchmark', type=int, required=False, default=1)
    parser.add_argument('-t', '--trace', help='number of times to repeat each benchmark', type=bool, required=False, default=False)
    parser.add_argument('-o', '--outfile', help='file to print to', type=str, required=False, default=None)

    args = parser.parse_args(argv[1:])

    if not pathlib.Path(args.config_file).is_file():
        raise FileNotFoundError(f'{args.config_file} was not found')

    sdl_path = pathlib.Path(args.sdl_file)
    if not sdl_path.is_file():
        raise FileNotFoundError(f'{args.sdl_file} was not found')

    outfile_path = None
    if args.outfile is not None:
        outfile_path = pathlib.Path(args.outfile)

    return SimulationArgs(config = get_configs(args.config_file),
                          config_file = args.config_file,
                          benchmarks = args.benchmarks,
                          parrot_levels = args.parrot_levels,
                          nruns = args.nruns,
                          trace = args.trace,
                          sdl = sdl_path,
                          outfile = outfile_path)

if __name__ == '__main__':
    print(parse(sys.argv))
