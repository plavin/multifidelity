BOOST=/nethome/plavin3/local/boost_1_82_0
all: main

main: main.cpp ftpjrg.hpp
	g++ -std=c++17 -Wall -Wno-parentheses -I${BOOST} main.cpp -o main

clean:
	rm -f main

.PHONY: all clean
