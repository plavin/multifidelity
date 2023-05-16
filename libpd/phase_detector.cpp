#include "phase_detector.hpp"

// Simplifed interfact to make it easier to call from Python
std::map<uint64_t, int64_t> run_pd(std::vector<uint64_t> addrs, double threshold, uint32_t interval_len, uint32_t log2_signature_len, uint32_t drop_bits) {

    PhaseDetector pd(threshold, interval_len, log2_signature_len, drop_bits);
    return pd.detect(addrs);
}
