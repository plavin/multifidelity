#!/usr/bin/env python3
import numpy as np
from dataclasses import dataclass

@dataclass
class Window:
    data: np.ndarray
    start: int = 0
    size: int = 1000

    def get(self, idx, debug=False):
        begin = self.start + self.size*idx
        end   = self.start + self.size + (self.size)*idx
        if debug:
            print(f'[start: {self.start}, size: {self.size}] -> [begin: {begin}, end: {end}]')
        if end > len(self.data):
            return None
        return self.data[range(begin, end)]

    def get_range(self, idx_begin, idx_end, debug=False):
        if idx_end - idx_begin < 1:
            return None

        begin = self.start + self.size*idx_begin
        end   = self.start + self.size + (self.size)*idx_end

        if debug:
            print(f'[start: {self.start}, size: {self.size}] -> [begin: {begin}, end: {end}]')
        if end > len(self.data):
            return None

        return self.data[range(begin, end)]

    def get_point(self, pt):
        # Return the location and value of the point
        return pt*self.size, self.data[pt*self.size]

    def shift_and_grow(self,shift, grow):
        # shift units: how many windows to shift by
        # grow units: how many datapoints to grow by
        self.start += self.size * shift
        self.size  += grow

    def shift_and_reset(self, shift, size):
        self.start += self.size * shift
        self.size = size

if __name__ == "__main__":
    data = np.array([i for i in range(100)])
    win = Window(data, start = 0, size = 10)
    tests = []
    tests.append(np.all(win.get(0) == np.array([i for i in range(10)])))
    tests.append((np.all(win.get_range(0, 1) == np.array([i for i in range(20)]))))
    tests.append((win.get_point(5) == (50, 50)))
    print(tests)
    win.shift_and_grow(1, 1)
    print(np.all(win.get(0) == np.array([i for i in range(10, 21)])))
    win.shift_and_reset(1, 10)
    print(np.all(win.get(0) == np.array([i for i in range(21, 31)])))
    print('Tests passed!')
