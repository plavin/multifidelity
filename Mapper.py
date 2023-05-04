#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

class Mapper:
    def __init__(self, size):
        self.size = size
        self.smallest_sq = int(np.ceil(np.sqrt(self.size)))

        # There will never be a non-full first row
        self.ncols = self.smallest_sq

        # If the last row would be completely empty, reduce this number
        # Only need enough rows to fit up to size elements
        self.nrows = int(np.ceil(self.size / self.ncols))

        self.fig, self.ax = plt.subplots(nrows = self.nrows, ncols=self.ncols, sharey=True)

    def get_remainder(self):
        # Any spots that wouldn't be full go here
        return [self._getitem(i, False) for i in range(self.size, self.nrows*self.ncols)]

    def _getitem(self, idx, check=True):
        if (idx >= self.size) and check:
            raise IndexError(f'Requested index ({idx}) outside configured range (0-{self.size-1}).')
        return self.ax[(idx//self.smallest_sq, idx % self.smallest_sq)]

    def __getitem__(self, idx):
        return self._getitem(idx)


if __name__ == "__main__":
    tests = []

    mp = Mapper(4)
    tests.append(mp.size == 4)
    tests.append(mp.smallest_sq == 2)
    tests.append(len(mp.get_remainder()) == 0)
    tests.append(mp[3] is not None)

    mp = Mapper(5)
    tests.append(mp.size == 5)
    tests.append(mp.smallest_sq == 3)
    tests.append(mp.nrows == 2)
    tests.append(mp.ncols == 3)
    tests.append(len(mp.get_remainder()) == 1)

    if np.all(tests):
        print('Tests passed!')
    else:
        for i, result in enumerate(tests):
            if not result:
                print(f'Test {i} failed')
