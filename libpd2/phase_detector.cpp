#include <cstdio>
#include <iostream>
#include "phase_detector.hpp"

int main ()
{
    PhaseDetector pd(0.5, 10, 10, 3);

    std::vector<uint64_t> test_addrs(10, 0);

    std::map<uint64_t, int64_t> phase_changes = pd.detect(test_addrs);
    for (const auto& pair : phase_changes) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

}
