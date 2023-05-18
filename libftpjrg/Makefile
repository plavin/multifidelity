BOOST=/nethome/plavin3/local/boost_1_66_0
all: main

main: ftpjrg.cpp ftpjrg.hpp
	g++ -std=c++17 -Wall -Wno-parentheses -I${BOOST} ftpjrg.cpp -o main

clean:
	rm -f main

.PHONY: all clean
