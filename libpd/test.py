#!/usr/bin/env python3

import sys
sys.path.insert(0, '/nethome/plavin3/sst/spec-utils/libpd/build')
import FastPhaseDetector

addr = [0]*105

phases = FastPhaseDetector.run_pd(addr, 0.5, 10, 10, 3)
print(phases)

