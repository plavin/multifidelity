#!/usr/bin/env python3
import statistics

def subsetter(data, tol=0.01):
    if len(data) == 1:
        return None, None

    ind = [x for _, x in sorted(zip(data, [*range(len(data))]))]
    ol = len(data)
    data = sorted(data)
    j = 0

    while len(data) > 1:
        # Phase 1: Remove from left side
        for i in range(len(data)-1):
            if statistics.stdev(data[i:]) < tol:
                return data[i:], ind[i:]

        # Phase 2: Remove from right side
        data = data[:-1]
        j += 1
    return None, None

def test(i, arr, truth):
    vals, ind = subsetter(arr)
    if truth is None and vals is None:
        print(f'Test {i} passed')
        return
    v2 = [arr[q] for q in ind]
    if vals != v2 or vals != truth:
        print(f'Test {i} failed')
        print(f'  Given:    {result}\n  Expected: {truth}')
    else:
        print(f'Test {i} passed')

if __name__ == "__main__":
    d0 = [66.01, 66.02, 0, 1, 2, 3, 45]
    test(0, d0, [66.01, 66.02])

    d1 = [0, 1, 2, 3, 4, 66.01, 66.02, 66.03, 5]
    test(1, d1, [66.01, 66.02, 66.03])

    d2 = [0, 66.01, 66.02, 66.03, 1, 2, 3, 4]
    test(2, d2, [66.01, 66.02, 66.03])

    d3 = [0, 1, 2, 3, 4, 66.01, 66.02, 66.03]
    test(3, d3, [66.01, 66.02, 66.03])

    d4 = [1]
    test(4, d4, None)

    d5 = [1, 2, 3, 4, 5]
    test(5, d5, None)
