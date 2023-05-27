#!/usr/bin/env python3

import pathlib
import pandas as pd
from functools import total_ordering

@total_ordering
class Trace:
    def __init__(self, path, new_ext=False):
        self.path = path
        self.name = path.name.split('.')[0].split('_')[2]
        self.data = None
        self.stable = None

        if new_ext:
            filename = self.path.name.replace('latency_trace', 'stable_region')
            self.stable_path = path.parent.joinpath(pathlib.Path(filename)).resolve()
            if self.stable_path.exists():
                self.stable = pd.read_csv(self.stable_path, delim_whitespace=True)

    def _load(self):
        return pd.read_csv(self.path, delim_whitespace=True)

    def load(self, persist=False):
        if self.data is not None:
            return self.data
        if persist:
            self.data = self._load()
            return self.data
        return self._load()

    def unload(self):
        self.data = None

    def __repr__(self):
        return self.name

    def __lt__(self, obj):
        return ((self.name) < (obj.name))

    def __eq__(self, obj):
        return (self.name == obj.name)

class TraceList:
    def __init__(self, data_dir, new_ext=False):
        if new_ext:
            self.files = [p.absolute() for p in pathlib.Path(data_dir).iterdir() if '.latency_trace' in p.suffixes]
        else:
            self.files = [p.absolute() for p in pathlib.Path(data_dir).iterdir()]

        self.traces = sorted([Trace(f, new_ext) for f in self.files])

    def __getitem__(self, idx):
        return self.traces[idx]

    def load(self):
        [tr.load(persist=True) for tr in self.traces]

    def unload(self):
        [tr.unload() for tr in self.traces]

    def __repr__(self):
        return " ".join([tr.__repr__() for tr in self.traces])

    def __len__(self):
        return len(self.traces)

    def __iter__(self):
        return iter(self.traces)

    def find(self, name):
        for t in self.traces:
            if t.name == name:
                return t
        return None

if __name__ == "__main__":
    DATA_DIR = 'parrot-traces/medium-100ms-manualpd/'
    TRACES = TraceList(DATA_DIR)
    print(TRACES)
