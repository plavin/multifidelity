cmake_minimum_required(VERSION 3.4...3.18)
project(example LANGUAGES CXX)

include_directories(/nethome/plavin3/local/boost_1_66_0)

add_subdirectory(pybind11)
pybind11_add_module(FastPhaseDetector phase_detector.cpp)
