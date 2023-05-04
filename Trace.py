#!/usr/bin/env python3

import pathlib
import pandas as pd
from functools import total_ordering

@total_ordering
class Trace:
    def __init__(self, path):
        self.path = path
        self.name = path.stem.split('_')[2]
        self.data = None

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
    def __init__(self, data_dir, max_files=None):
        self.files = [p.absolute() for p in pathlib.Path(data_dir).iterdir()]
        if max is not None:
            self.files = self.files[:max_files]
        self.traces = sorted([Trace(f) for f in self.files])

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

if __name__ == "__main__":
    DATA_DIR = 'parrot-traces/medium-100ms-manualpd/'
    TRACES = TraceList(DATA_DIR)
    print(TRACES)
