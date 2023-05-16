#include <iostream>
#include <numeric>
#include "phase_detector.hpp"

int main() {

    double threshold = 0.5;
    uint32_t interval_len = 10;
    uint32_t log2_signature_len = 10;
    uint32_t drop_bits = 3;

    std::vector<uint64_t> addrs(105, 0);

    std::iota(addrs.begin(), addrs.end(), 1);

    std::map<uint64_t, int64_t> phase_changes = detect(addrs, threshold, interval_len, log2_signature_len, drop_bits);

    for (const auto& pair : phase_changes) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }


}
