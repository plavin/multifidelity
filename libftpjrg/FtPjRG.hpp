#include <iostream>
class FtPjRG() {
    private:
        int window_start  = 1000;
        int summarize     = 1000;
        int ms_init       = 10;
        bool debug        = False;
        int disp_interval = 100000;

        // F-test parameters
        float f_conf = 0.05;
        int f_shift  = 1;
        int f_grow   = 1;

        // t-test parameters
        float t_conf  = 0.05;
        int t_shift   = 1;
        int t_grow    = 1;

        // Projection test parameters
        int proj_dist    = 5;
        float proj_delta = 1.0;
        int p_shift      = 1;
        int p_grow       = 1;
        int p_j          = 1;

    public:
        FtPjRG() {

        }

        long run(std::vector<uint64_t> data) {
            uint64_t new_len = data.size() / summarize;
            std::vector<double> data_summ(new_len);
            for (int i = 0; i < new_len; i++) {
                data_summ[i] = std::reduce(data.begin()+(i  )*summarize,
                                           data.begin()+(i+1)*summarize) / summarize;
            }

            for (int i = 0; i < data_summ.size(); i++) {
                std::cout << data_summ.at(i) << ' ';
            }
            std::count << std::endl;
            return 0;

        }

};
