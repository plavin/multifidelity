#ifdef PYBIND
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#endif //PYBIND
#include <boost/random/normal_distribution.hpp>
#include <boost/random/mersenne_twister.hpp>
#include "ftpjrg.hpp"

std::tuple<uint64_t,uint64_t,bool> run_with_settings(std::vector<uint64_t> data, uint64_t window_start, int summarize, int proj_dist, float proj_delta, int p_j) {
    FtPjRG ft(window_start, summarize, proj_dist, proj_delta, p_j);
    return ft.run(data);
}

std::tuple<uint64_t,uint64_t,bool> run(std::vector<uint64_t> data) {
    FtPjRG ft;
    return ft.run(data);
}

#ifdef PYBIND
namespace py = pybind11;

PYBIND11_MODULE(FastFtpjrg, m) {
    m.doc() = "A module implementing the FtPjRG method";
    m.def("run", &run, "Run the FtPjRG method", py::arg("data"));
    m.def("run_with_settings", &run_with_settings, "Run the FtPjRG method", py::arg("data"), py::arg("window_start"), py::arg("summarize"), py::arg("proj_dist"), py::arg("proj_delta"), py::arg("p_j"));
}
#endif //PYBIND
