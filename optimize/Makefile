BOOST=/nethome/plavin3/local/boost_1_82_0/install

all: optimize

optimize: main.cc
	g++ -g -O0 main.cc -std=c++17 -fopenmp -I${BOOST}/include -L${BOOST}/lib -lboost_system -lboost_filesystem -I../libpd -I../libftprjg -o optimize

test: optimize
	./optimize ../parrot-traces/polybench-v0.1-test/

clean:
	rm -rf optimize

.PHONY: all clean test
