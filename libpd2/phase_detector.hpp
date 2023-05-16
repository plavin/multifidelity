#include <cmath>
#include <map>
#include <boost/dynamic_bitset.hpp>

using bitvec = boost::dynamic_bitset<>;

class PhaseDetector {
    private:
        bitvec sig;

        // Parameters
        float threshold;
        uint32_t interval_len;
        uint32_t signature_len;
        uint32_t log2_signature_len;
        uint32_t drop_bits;
        uint32_t stable_min;

        // Variables
        uint64_t instruction_count = 0;
        uint64_t stable_count = 0;
        uint64_t last_ip = 0;

        // Functions
        uint64_t hash_address(uint64_t x) {
            // Drop low bits
            x = x >> drop_bits;

            // Do the hash
            // Ref: https://stackoverflow.com/a/12996028
            x = (x ^ (x >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
            x = (x ^ (x >> 27)) * UINT64_C(0x94d049bb133111eb);
            x = x ^ (x >> 31);

            // Chop to only log2_sig_len bits
            x = x >> (64 - log2_signature_len);
            return x;
        }

        double diff_sig(bitvec sig1, bitvec sig2) {
            return static_cast<double>((sig1 ^ sig2).count()) / (sig1 | sig2).count();
        }

    public:
        PhaseDetector(float threshold, uint32_t interval_len, uint32_t log2_signature_len, uint32_t drop_bits) :
            threshold(threshold),
            interval_len(interval_len),
            log2_signature_len(log2_signature_len),
            drop_bits(drop_bits)
        {
            signature_len = pow(2, log2_signature_len);
            sig = boost::dynamic_bitset<>(signature_len);
        }

        std::map<uint64_t, int64_t> detect(std::vector<uint64_t> x) {
            std::map<uint64_t, int64_t> phase_change;
            phase_change[10] = -1;
            return phase_change;
        }

};
