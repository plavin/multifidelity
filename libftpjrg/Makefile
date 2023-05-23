BOOST=/nethome/plavin3/local/boost_1_82_0
all: main libftpjrg.so

ftpjrg.o: ftpjrg.cpp ftpjrg.hpp
	g++ -std=c++17 -Wall -Wno-parentheses -I${BOOST} ftpjrg.cpp -fPIC -c -o ftpjrg.o

main: ftpjrg.o
	g++ -std=c++17 -Wall -Wno-parentheses -I${BOOST} main.cpp ftpjrg.o -o main

libftpjrg.so: ftpjrg.o
	g++ -std=c++17 -Wall -Wno-parentheses -I${BOOST} ftpjrg.o -fPIC -shared -o libftpjrg.so

clean:
	rm -f main libftpjrg.so ftpjrg.o

.PHONY: all clean
