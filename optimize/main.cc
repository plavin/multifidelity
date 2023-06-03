#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <omp.h>

// Boost includes
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>
#include <boost/filesystem/fstream.hpp>
namespace fs = boost::filesystem;

struct trace {
    std::vector<uint64_t> ip;
    std::vector<uint64_t> latency_nano;
};

/*
using score = std::pair<double, double>;

score 
*/

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

    std::vector<trace> traces;
    #pragma omp parallel for
    for (int i = 0; i < trace_file_paths.size(); i++) {
        std::cout << trace_file_paths[i].filename() << std::endl;
        traces.push_back(load(trace_file_paths[i], 1000));
    }

    for (int i = 0; i < 10; i++) {
        std::cout << traces[0].ip[i] << std::endl;
    }


}
