cmake_minimum_required(VERSION 3.4...3.18)
project(FastPhaseDetector LANGUAGES CXX)

include_directories(/nethome/plavin3/local/boost_1_66_0)

find_package(OpenMP)
link_libraries(OpenMP::OpenMP_CXX)

add_subdirectory(pybind11)
pybind11_add_module(FastPhaseDetector phase_detector.cpp)
