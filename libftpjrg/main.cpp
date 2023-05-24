#include <boost/random/normal_distribution.hpp>
#include <boost/random/mersenne_twister.hpp>
#include "ftpjrg.hpp"

void test1() {
    FtPjRG ft;


    std::vector<uint64_t> xs(4000000);
    for (auto &i: xs) {
        i = 10;
    }
    for (auto ip = xs.begin()+xs.size()/2; ip!=xs.end(); ip++) {
        *ip = 20;
    }
    auto ret = ft.run(xs);
    if (std::get<2>(ret)) {
        //std::cout << "Converged at " << *stable << std::endl;
        std::cout <<" Converged.\n";
    } else {
        std::cout << "main: Never converged!\n";
    }

}

void test2()
{
    FtPjRG ft;
    boost::random::normal_distribution dist;
    boost::random::mt19937 rng;

    std::vector<uint64_t> data(4000000);
    for (auto &x : data) {
        x = rng() % 100;
    }

    for (auto ip = data.begin()+1000000; ip!=data.end(); ip++) {
        *ip = 100 + rng() % 200;
    }

    std::cout << "Calling ft.run\n";
    ft.run(data);

}

int main() {
    test2();
}
