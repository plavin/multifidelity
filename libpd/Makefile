all: main

BOOST=/nethome/plavin3/local/boost_1_66_0
CXXFLAGS=-fopenmp -O3 -fPIC -I${BOOST} -I/nethome/plavin3/sst/venv/lib/python3.6/site-packages/pybind11/include/

phase_detector.o: phase_detector.cpp phase_detector.hpp
	g++ ${CXXFLAGS} -fopenmp -c -o phase_detector.o phase_detector.cpp

libpd.so: phase_detector.o
	g++ -shared -o libpd.so phase_detector.o

main: main.cpp libpd.so
	g++ ${CXXFLAGS} -L. -lpd main.cpp -o main

clean:
	rm -f main libpd.so phase_detector.o

.PHONY: clean all
