#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <omp.h>
#include <algorithm>

// Local includes
#include "../libpd/phase_detector.hpp"
#include "../libftpjrg/ftpjrg.hpp"

// Boost includes
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>
#include <boost/filesystem/fstream.hpp>
namespace fs = boost::filesystem;

#define DEBUG

// Globals
int PD_WINDOW = 10'000;

struct trace {
    std::vector<uint64_t> ip;
    std::vector<uint64_t> latency_nano;
};

trace load(fs::path p, uint64_t max=0) {
    fs::ifstream file(p);

    std::string line;
    uint64_t ip, threadID, addr, latency_nano;
    int64_t phase;
    char rwf;
    trace t;

    // skip header
    getline(file, line);

    int read = 0;
    while (getline(file, line)) {
        std::istringstream iss(line);
        iss >> ip >> phase >> rwf >> threadID >> addr >> latency_nano;
        t.ip.push_back(ip);
        t.latency_nano.push_back(latency_nano);
        if (max) {
            if (read++ > max) {
                file.close();
                return t;
            }
        }
    }

    file.close();
    return t;
}

struct PhaseData {
    bool has_rr = false;
    double rr_mean = 0.0;
    double overall_mean = 0.0;
    double pct_error = 0.0;
    uint64_t accesses_after_rr = 0;
};

using score = std::pair<double, double>; // pct swapped, RR accuracy

score eval(const trace &tr, PhaseDetector &pd, FtPjRG &sd) {

    // Run phase detection
    std::map<uint64_t, int64_t> phase_map = pd.detect(tr.ip);
    // append an extra entry to represent the end of the trace to simplify algo
    phase_map[tr.ip.size()] = -1;

#ifdef DEBUG
    printf(" Phase map:\n");
    for (auto &[k, v] : phase_map) {
        std::cout << "  " << k << ": " << v << "\n";
    }
#endif

    // Find RRs but running the stability detector on the first occurence of each phase
    // Don't treat -1 separately in this algorithm. We need it to count negatively against our score
    // But don't run the SD
    std::map<int64_t, PhaseData> phase_data;
    uint64_t last_access = 0;

    int64_t  current_phase = 0;

    int64_t  last_phase = 0;
    uint64_t current_start = 0;
    uint64_t current_end = 0;

    bool first = true;

    for (auto const& [access, phase_id] : phase_map)
    {
        current_start = last_access;

        uint64_t phase_length = access - last_access;
        current_end = last_access + phase_length;;
        last_access = access;

        current_phase = last_phase;
        last_phase = phase_id;


        if (first || current_phase == -1) {
            first = false;
            continue;
        }

        if (phase_data.find(current_phase) != phase_data.end()) {
            //phase encountered before
            auto &cur = phase_data[current_phase];
            if (cur.has_rr) {
                cur.accesses_after_rr += phase_length;
            }
        } else {
            PhaseData phd;

            // Run SD
            const auto &[win_start0, win_size, rr_found] = sd.run(std::vector<uint64_t>(tr.latency_nano.begin() + current_start, tr.latency_nano.begin()+current_end));

            if (rr_found) {

#ifdef DEBUG
                std::cout << "   Phase " << current_phase << " rr: " << win_start0 << ", " << win_size << std::endl;
#endif

                uint64_t win_start = win_start0 + current_start;
                uint64_t win_end = win_start + win_size;


                phd.has_rr = true;
                phd.rr_mean = std::accumulate(tr.latency_nano.begin()+win_start,
                                              tr.latency_nano.begin()+win_end,
                                              0.0) / (win_size);
                phd.overall_mean = std::accumulate(tr.latency_nano.begin()+current_start,
                                                   tr.latency_nano.begin()+current_end,
                                                   0.0) / (phase_length);
                phd.accesses_after_rr = current_end - win_end;
                phd.pct_error = abs(100*(phd.rr_mean - phd.overall_mean) / phd.overall_mean);
            } else {

#ifdef DEBUG
                std::cout << "   Phase " << current_phase << " NO RR" << std::endl;
#endif

                phd.has_rr = false;
            }
            phase_data[current_phase] = phd;
        }

    }

    // total time is length of trace
    // time swapped is sum of phd.accesses_after_rr if phd.has_rr
    uint64_t time_swapped = 0;
    double sum_error = 0;
    for (auto const& [phase_id, phd] : phase_data) {
        if (phd.has_rr){
            time_swapped += phd.accesses_after_rr;
            sum_error += phd.accesses_after_rr*phd.pct_error;
        }
    }

    if (time_swapped == 0) {
        return score(0, 0); //zero percent swapped, but zero error as well
    }

    double pct_swapped = ((double)time_swapped) / tr.ip.size();
    double rr_accuracy = sum_error / time_swapped; // normalize based on time each was used
    return score(pct_swapped, rr_accuracy);
}

score eval_traces(const std::vector<trace> &traces, PhaseDetector &pd, FtPjRG &sd) {
    std::vector<score> scores;
    uint64_t total_length = 0;
#ifdef DEBUG
    int _i = 0;
#endif
    for (auto &tr : traces) {
#ifdef DEBUG
        std::cout << "Trace " << _i++ << " - - - - -" << std::endl;
#endif
        scores.push_back(eval(tr, pd, sd));
        total_length += tr.ip.size();
    }
    double sum_pct_swapped = 0;
    double sum_rr_accuracy = 0;
    int i = 0;
    for (auto &[pct_swapped, rr_accuracy] : scores){
        sum_pct_swapped += pct_swapped*traces[i].ip.size();
        sum_rr_accuracy += rr_accuracy;
        i++;
    }

#ifdef DEBUG
    printf("Scores:");
    for (auto &[pct, acc] : scores) {
        std::cout << " (" << pct << ", " << acc << ")";
    }
    printf("\n");
#endif

    return score(sum_pct_swapped/total_length, sum_rr_accuracy/scores.size());
}

score eval_traces_nonormilaize(const std::vector<trace> &traces, PhaseDetector &pd, FtPjRG &sd) {
    std::vector<score> scores;
    for (auto &tr : traces) {
        scores.push_back(eval(tr, pd, sd));
    }
    double sum_pct_swapped = 0;
    double sum_rr_accuracy = 0;
    for (auto &[pct_swapped, rr_accuracy] : scores){
        sum_pct_swapped += pct_swapped;
        sum_rr_accuracy += rr_accuracy;
    }
    return score(sum_pct_swapped/scores.size(), sum_rr_accuracy/scores.size());
}

int main(int argc, char** argv) {

    bool have_outfile = false;

    if (argc < 2) {
        std::cout << "Usage: ./optimize <trace-directory>" << std::endl;
        exit(1);
    }

    fs::path trace_path(argv[1]);

    if (!fs::is_directory(trace_path)) {
        std::cout << "Error: " << argv[1] << " is not a directory.\n";
    }

    // Old defaults
    /*
    std::vector<int> param_phase_length{10'000};
    std::vector<double> param_threshold{0.5};
    std::vector<int> param_stable_min{4};
    std::vector<uint64_t> param_window_start{10};
    std::vector<int> param_summarize{500};
    std::vector<int> param_proj_dist{5};
    std::vector<float> param_proj_delta{2.0};
    std::vector<int> param_p_j{4};
    */

    // New Config
    std::cout << "# New config\n";
    std::vector<int> param_phase_length{10'000};
    std::vector<double> param_threshold{0.5};
    std::vector<int> param_stable_min{3};
    std::vector<uint64_t> param_window_start{50};
    std::vector<int> param_summarize{1000};
    std::vector<int> param_proj_dist{5};
    std::vector<float> param_proj_delta{1.0};
    std::vector<int> param_p_j{4};

    // First run
    /*
    // Phase detection parameters
    std::vector<int> param_phase_length{10'000, 50'000, 100'000, 200'000};
    std::vector<double> param_threshold{0.4, 0.5, 0.6};
    std::vector<int> param_stable_min{3, 4, 5};


    // Stability detection parameters
    std::vector<uint64_t> param_window_start{10, 15, 20};
    std::vector<int> param_summarize{250, 500, 1000};
    std::vector<int> param_proj_dist{5, 10};
    std::vector<float> param_proj_delta{0.5, 1.0, 2.0};
    std::vector<int> param_p_j{4, 6, 8, 10};
    */

    // Second run
    // Phase detection parameters
    /*
    std::vector<int> param_phase_length{50'000};
    std::vector<double> param_threshold{0.6, 0.65};
    std::vector<int> param_stable_min{3};


    // Stability detection parameters
    std::vector<uint64_t> param_window_start{20, 25};
    std::vector<int> param_summarize{1000, 1500};
    std::vector<int> param_proj_dist{5, 10};
    std::vector<float> param_proj_delta{0.5, 1.0, 2.0};
    std::vector<int> param_p_j{4, 6, 8, 10};
    */

    // Third run
    // Phase detection parameters
    /*
    std::vector<int> param_phase_length{10'000, 50'000, 100'000};
    std::vector<double> param_threshold{0.5, 0.6, 0.65};
    std::vector<int> param_stable_min{3};


    // Stability detection parameters
    std::vector<uint64_t> param_window_start{20, 25, 50};
    std::vector<int> param_summarize{1000, 1500};
    std::vector<int> param_proj_dist{5, 10};
    std::vector<float> param_proj_delta{0.5, 1.0, 2.0};
    std::vector<int> param_p_j{4, 6, 8, 10};
    */


    std::cout << "# Testing " << param_phase_length.size() * param_threshold.size() * param_stable_min.size() *
                               param_window_start.size() * param_summarize.size() * param_proj_dist.size() *
                               param_proj_delta.size() * param_p_j.size()
                            << " configurations \n";

    std::vector<fs::path> trace_file_paths;
    for(auto& entry : boost::make_iterator_range(fs::directory_iterator(trace_path), {})) {
        if (fs::is_regular_file(entry) && entry.path().string().find("trace.out") != std::string::npos){
            trace_file_paths.push_back(entry.path());
        }
    }

    std::cout << "# Reading [" << trace_file_paths.size() << "] trace.out files from [" << trace_path.string() << "]\n";

    // Step 1: Read in traces
    std::vector<trace> traces;
    //TODO: change back
    for (int i = 0; i < trace_file_paths.size(); i++) {
    //for (int i = 0; i < 20; i++) {
        std::cout << "# -> " << trace_file_paths[i].filename().string() << std::endl;
        traces.push_back(load(trace_file_paths[i]));
    }

    std::cout << "# Done loading files.\n";

    // Output header
    std::cout  << "pct "
               << "acc "
               << "threshold "
               << "phase_length "
               << "stable_min "
               << "window_start "
               << "summarize "
               << "proj_dist "
               << "proj_delta "
               << "p_j" << std::endl;

    #pragma omp parallel for collapse(8)
    for (int i0 = 0; i0 < param_phase_length.size(); i0++) {
        for (int i1 = 0; i1 < param_threshold.size(); i1++) {
            for (int i2 = 0; i2 < param_stable_min.size(); i2++) {
                for (int i3 = 0; i3 < param_window_start.size(); i3++) {
                    for (int i4 = 0; i4 < param_summarize.size(); i4++) {
                        for (int i5 = 0; i5 < param_proj_dist.size(); i5++) {
                            for (int i6 = 0; i6 < param_proj_delta.size(); i6++) {
                                for (int i7 = 0; i7 < param_p_j.size(); i7++) {
                                    auto pl = param_phase_length[i0];
                                    auto th = param_threshold[i1];
                                    auto sm = param_stable_min[i2];
                                    auto ws = param_window_start[i3];
                                    auto sum = param_summarize[i4];
                                    auto di = param_proj_dist[i5];
                                    auto de = param_proj_delta[i6];
                                    auto pj = param_p_j[i7];
                                    PhaseDetector pd(th, pl, 10, sm);
                                    FtPjRG sd(ws, sum, di, de, pj);
                                    score sc = eval_traces(traces, pd, sd);
                                    #pragma omp critical
                                    {
                                    std::cout << sc.first  << " "
                                              << sc.second << " "
                                              << th        << " "
                                              << pl        << " "
                                              << sm        << " "
                                              << ws        << " "
                                              << sum       << " "
                                              << di        << " "
                                              << de        << " "
                                              << pj        << std::endl;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
