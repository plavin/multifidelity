BOOST=/nethome/plavin3/local/boost_1_82_0

all: optimize

optimize: main.cc
	gcc -I${BOOST} main.cc -Wall -Wextra -o optimize

test: optimize
	./optimize ../parrot-traces/polybench-v0.1-test/

clean:
	rm -rf optimize

.PHONY: all clean test
