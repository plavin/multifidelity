cmake_minimum_required(VERSION 3.4...3.18)
set(CMAKE_CXX_STANDARD 17)
set(CXX_STANDARD 17)
project(Ftpjrg LANGUAGES CXX)
include_directories(/nethome/plavin3/local/boost_1_82_0)


add_subdirectory(pybind11)

pybind11_add_module(FastFtpjrg ftpjrg.cpp)

