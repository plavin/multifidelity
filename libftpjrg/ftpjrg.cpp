#include "ftpjrg.hpp"

int main() {
    FtPjRG ft;
    std::vector<uint64_t> xs(4000000);
    for (auto &i: xs) {
        i = 10;
    }
    for (auto ip = xs.begin()+xs.size()/2; ip!=xs.end(); ip++) {
        *ip = 20;
    }
    if (auto stable = ft.run(xs) ) {
        //std::cout << "Converged at " << *stable << std::endl;
        std::cout <<" Converged.\n";
    } else {
        std::cout << "main: Never converged!\n";
    }
    
}
