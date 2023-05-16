phase_detector.o: phase_detector.cpp phase_detector.hpp
	g++ -c -o phase_detector.o
main: phase_detector.cpp phase_detector.hpp
	g++ -fopenmp -std=c++2a -I/nethome/plavin3/local/boost_1_66_0 phase_detector.cpp -o main

.PHONY: clean

clean:
	rm -f main

