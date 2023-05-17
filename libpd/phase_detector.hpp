#include <cmath>
#include <map>
#include <boost/dynamic_bitset.hpp>
#include <iostream>

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
        PhaseDetector(float threshold, uint32_t interval_len, uint32_t log2_signature_len, uint32_t stable_min) :
            threshold(threshold),
            interval_len(interval_len),
            log2_signature_len(log2_signature_len),
            stable_min(stable_min)
        {
            signature_len = pow(2, log2_signature_len);
            drop_bits = 3;
            /*
            std::cout << "threshold: " << threshold << std::endl;
            std::cout << "interval_len: " << interval_len << std::endl;
            std::cout << "log2_signature_len: " << log2_signature_len << std::endl;
            std::cout << "signature_len: " << signature_len << std::endl;
            std::cout << "stable_min: " << stable_min << std::endl;
            std::cout << "drop_bits: " << drop_bits << std::endl;
            */
        }

        bitvec make_sig(std::vector<uint64_t>::iterator start, std::vector<uint64_t>::iterator end) {
            bitvec bv(signature_len);
            for (auto it = start; it != end; it++) {
                bv[hash_address(*it)] = 1;
            }
            return bv;
        };

        std::map<uint64_t, int64_t> detect(std::vector<uint64_t> xs) {

            // Map of phase changes
            std::map<uint64_t, int64_t> phase_changes;
            phase_changes[0] = 2; // Start in transition phase

            uint64_t nintervals = xs.size() / interval_len;
            std::vector<bitvec> sigs(nintervals);

            // Pre-compute all signatures since this is easy to do in parallel
#pragma omp parallel for
            for (uint64_t i = 0; i < nintervals; i++) {
                sigs[i] = make_sig(xs.begin()+i*interval_len, xs.begin()+(i+1)*interval_len);
            }

            int stable_count = 0;
            int phase = -1;
            int last_phase = -1;
            std::vector<bitvec> phase_table;

            for (uint64_t i = 1; i < nintervals; i++) {

				if (diff_sig(sigs[i-1], sigs[i]) < threshold) {
                    stable_count += 1;
                    if (stable_count >= stable_min && phase == -1) {
                        phase_table.push_back(sigs[i]);
                        phase = phase_table.size() - 1;
                    }
                } else {
                    stable_count = 0;
                    phase = -1;

                    if (!phase_table.empty()) {
                        double best_diff = threshold;
                        for (auto it = phase_table.begin(); it!=phase_table.end(); it++) {
                            double diff = diff_sig(sigs[i], *it);
                            if (diff < best_diff) {
                                phase = std::distance(phase_table.begin(), it);
                                best_diff = diff;
                            }
                        }
                    }

                }

                if (phase != last_phase) {
                    phase_changes[i*interval_len] = phase;
                }
                last_phase = phase;

            }

            return phase_changes;
        }
};

std::map<uint64_t, int64_t> run_pd(std::vector<uint64_t>, double, uint32_t, uint32_t, uint32_t);
