#ifdef PYBIND
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#endif //PYBIND
#include <boost/random/normal_distribution.hpp>
#include <boost/random/mersenne_twister.hpp>
#include "ftpjrg.hpp"

std::pair<uint64_t, uint64_t> run(std::vector<uint64_t> data) {
    FtPjRG ft;
    auto ret = ft.run(data);
    if (!ret) {
        return std::make_pair(0,0);
    } else {
        return *ret;
    }
}

#ifdef PYBIND
namespace py = pybind11;

PYBIND11_MODULE(FastFtpjrg, m) {
    m.doc() = "A module implementing the FtPjRG method";
    m.def("run", &run, "Run the FtPjRG method", py::arg("data"));
}
#endif //PYBIND
