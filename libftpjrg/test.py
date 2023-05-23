#!/usr/bin/env python3

import sys
sys.path.insert(0,'./build')
import FastFtpjrg
sys.path.insert(0,'./..')
from Trace import TraceList
import stackprinter
stackprinter.set_excepthook(style='lightbg3')
import numpy as np

DATA_DIR='../parrot-traces/medium-test'
TRACES = TraceList(DATA_DIR)
print('Files: ', TRACES)

for t in TRACES:
    if t.name != '2mm':
        continue
    print(f'Loading {t.name}')
    data = np.array(t.load()['latency_nano'], dtype=np.uint64)
    print(f'Running {t.name}')
    ret = FastFtpjrg.run(data)
    print(f'{t.name}: {ret}')
