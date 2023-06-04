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

// Globals
int MAX_ITER = 4;
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
                return t;
            }
        }
    }

    return t;
}

struct PhaseData {
    bool has_rr = false;
    double rr_mean = 0.0;
    double overall_mean = 0.0;
    uint64_t accesses_after_rr = 0;
};

using score = std::pair<double, double>; // pct swapped, RR accuracy

score eval(const trace &tr, PhaseDetector pd, FtPjRG sd) {

    // Run phase detection
    std::map<uint64_t, int64_t> phase_map = pd.detect(tr.ip);
    // append an extra entry to represent the end of the trace to simplify algo
    phase_map[tr.ip.size()] = -1;

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

        std::cout << current_phase << ": [" << current_start << "->" << current_end <<"]" << std::endl;

        //if ((auto &cur = phase_data.find(current_phase)) != phase_data.end()) {
        bool huh = phase_data.find(current_phase) != phase_data.end();
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

            std::cout << "Phase " << current_phase << ": " << rr_found << std::endl;
            if (rr_found) {
                uint64_t win_start = win_start0 + current_start;
                uint64_t win_end = win_start + win_size;

                std::cout << " Extents: " << win_start << ", " << win_end << std::endl;

                phd.has_rr = true;
                phd.rr_mean = std::accumulate(tr.latency_nano.begin()+win_start,
                                              tr.latency_nano.begin()+win_end,
                                              0.0) / (win_size);
                phd.overall_mean = std::accumulate(tr.latency_nano.begin()+current_start,
                                                   tr.latency_nano.begin()+current_end,
                                                   0.0) / (phase_length);
                phd.accesses_after_rr = current_end - win_end;
                std::cout << " Means: " << phd.rr_mean << ", " << phd.overall_mean << std::endl;
            } else {
                phd.has_rr = false;
            }
            phase_data[current_phase] = phd;
        }

    }

    double pct_swapped = 0.0;
    double rr_accuracy = 0.0;
    return score(pct_swapped, rr_accuracy);
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

    std::cout << "Reading *trace.out files from [" << trace_path << "]\n";

    std::vector<fs::path> trace_file_paths;
    for(auto& entry : boost::make_iterator_range(fs::directory_iterator(trace_path), {})) {
        if (fs::is_regular_file(entry) && entry.path().string().find("trace.out") != std::string::npos){
            trace_file_paths.push_back(entry.path());
        }
    }

    // Step 1: Read in traces
    std::vector<trace> traces;
    #pragma omp parallel for
    //TODO: change back
    //for (int i = 0; i < trace_file_paths.size(); i++) {
    for (int i = 0; i < 1; i++) {
        std::cout << trace_file_paths[i].filename() << std::endl;
        traces.push_back(load(trace_file_paths[i]));
    }


    // Step 2: Run PD and SD
    PhaseDetector pd(0.5, PD_WINDOW, 10, 4);
    FtPjRG sd;
    eval(traces[0], pd, sd);
    /*
    for (int iter = 0; iter < 1; iter++) {
        
    }
    */
}
