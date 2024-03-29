#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "phase_detector.hpp"

// Simplifed interface to make it easier to call from Python
std::map<uint64_t, int64_t> run_pd(std::vector<uint64_t> addrs, double threshold, uint32_t interval_len, uint32_t log2_signature_len, uint32_t stable_min) {

    PhaseDetector pd(threshold, interval_len, log2_signature_len, stable_min);
    return pd.detect(addrs);
}

namespace py = pybind11;

PYBIND11_MODULE(FastPhaseDetector, m) {
    m.doc() = "A module providing fast phase detection."; // optional module docstring

    m.def("run_pd", &run_pd, "Run the phase detector on a vector of addresses",
            py::arg("addrs"), py::arg("threshold"), py::arg("interval_len"), py::arg("log2_signature_len"), py::arg("stable_min"));
}
