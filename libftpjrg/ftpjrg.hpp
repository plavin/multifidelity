#include <vector>
#include <iostream>
#include <functional>
#include <numeric>
#include <optional>

#include <boost/math/distributions/fisher_f.hpp>
#include <boost/math/distributions/students_t.hpp>
using boost::math::fisher_f;
using boost::math::students_t;

template <typename T>
using WinRange = std::optional<std::pair<typename std::vector<T>::iterator, typename std::vector<T>::iterator>>;

template <typename T>
using WinPoint = std::optional<std::pair<uint64_t, T>>;

template <typename T>
double calc_mean(WinRange<T> win) {
    auto begin = std::get<0>(*win);
    auto end   = std::get<1>(*win);
    auto size  = std::distance(begin, end);

    return std::accumulate(begin, end, 0.0) / size;

}

template <typename T>
double stddev(WinRange<T> win)
{
    auto begin = std::get<0>(*win);
    auto end   = std::get<1>(*win);
    auto size  = std::distance(begin, end);

    double mean = calc_mean<T>(win);
    double sq_sum = std::inner_product(begin, end, begin, 0.0,
        [](double const & x, double const & y) { return x + y; },
        [mean](double const & x, double const & y) { return (x - mean)*(y - mean); });
    return std::sqrt(sq_sum / size);
}

// Whether the variances are equal
// ref: https://www.boost.org/doc/libs/1_67_0/libs/math/example/f_test.cpp
template <typename T>
bool f_test(
        WinRange<T> win0,
        WinRange<T> win1,
        double alpha)  // Significance level
{
    double sd1 = stddev<T>(win0);
    double sd2 = stddev<T>(win1);

    double N1 = std::distance(std::get<0>(*win0), std::get<1>(*win0));
    double N2 = std::distance(std::get<0>(*win1), std::get<1>(*win1));

    double F = (sd1 / sd2);
    F *= F;
    fisher_f dist(N1 - 1, N2 - 1);

    // Two-sided test
    double ucv2 = quantile(complement(dist, alpha / 2));
    double lcv2 = quantile(dist, alpha / 2);

    // If true, don't reject, meaning variances are equal
    return (ucv2 < F) || (lcv2 > F);
}

// Whether the means are equal
// ref: https://www.boost.org/doc/libs/1_43_0/libs/math/doc/sf_and_dist/html/math_toolkit/dist/stat_tut/weg/st_eg/two_sample_students_t.html
template <typename T>
bool t_test(
        WinRange<T> win0,
        WinRange<T> win1,
        double alpha)  // Significance level
{
    double sd1 = stddev<T>(win0);
    double sd2 = stddev<T>(win1);

    double sm1 = calc_mean<T>(win0);
    double sm2 = calc_mean<T>(win1);

    double N1 = std::distance(std::get<0>(*win0), std::get<1>(*win0));
    double N2 = std::distance(std::get<0>(*win1), std::get<1>(*win1));

    // dof
    double v = N1 + N2 - 2; //dof
    // pooled variance
    double sp = sqrt(((N1-1) * sd1 * sd1 + (N2-1) * sd2 * sd2) / v);
    // t-stat
    double t_stat = (sm1 - sm2) / (sp * sqrt(1.0 / N1 + 1.0 / N2));

    students_t dist(v);
    return cdf(complement(dist, fabs(t_stat))) < alpha / 2;

}

template<typename T>
class Window {

private:
    std::vector<double> data;
    uint64_t start;

public:
    uint64_t size;
    Window(std::vector<T> data, uint64_t start, uint64_t size) : data(data), start(start), size(size) {
    }

    WinRange<T> get(uint64_t idx) {
        uint64_t begin = start + size * (idx  );
        uint64_t end   = start + size * (idx+1);
        return end <= data.size() ? WinRange<T>{std::make_pair(data.begin()+begin, data.begin()+end)} : std::nullopt;
    }

    WinRange<T> get_range(uint64_t idx_begin, uint64_t idx_end) {
        if (idx_end - idx_begin < 1) {
            return std::nullopt;
        }

        uint64_t begin = start + size    *idx_begin;
        uint64_t end   = start + (1+size)*idx_end; //inclusive!

        return end <= data.size() ? WinRange<T>{std::make_pair(data.begin()+begin, data.begin()+end)} : std::nullopt;

    }

    WinPoint<T> get_point (uint64_t pt) {
        uint64_t ind = pt * size;
        return ind <= data.size() ? WinPoint<T>{std::make_pair(ind, data[ind])} : std::nullopt;

    }

    void shift_and_grow(uint64_t shift, uint64_t grow) {
        start += size*shift;
        size += grow;
    }

    void shift_and_reset(uint64_t shift, uint64_t reset) {
        start += size*shift;
        size = size;
    }

};

class FtPjRG {
    private:
        uint64_t window_start  = 1000;
        int summarize     = 1000;
        int ms_init       = 10;
        bool debug        = false;
        int disp_interval = 100000;
        float g_m         = 1.1;

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

        std::optional<uint64_t> run(std::vector<uint64_t> data) {
            uint64_t new_len = data.size() / summarize;
            std::vector<double> data_summ(new_len);
            for (uint64_t i = 0; i < new_len; i++) {
                data_summ[i] = std::accumulate(data.begin()+(i  )*summarize, data.begin()+(i+1)*summarize, 0, std::plus<uint64_t>()) / summarize;
            }

            Window<double> win(data_summ, 0, window_start);

            WinRange<double> win0 = std::nullopt;
            WinRange<double> win1 = std::nullopt;
            uint64_t ms = ms_init;
            int _phase = 1;
            bool equal_variance = false;
            bool equal_mean = false;

            while (true) {
                switch (_phase) {
                    case 1:
                        win0 = win.get(0);
                        win1 = win.get(1);

                        if (!win1) {
                            std::cout << "FtPjRG: Never converged!\n";
                            return std::nullopt;
                        }
                        equal_variance = f_test<double>(win0, win1, f_conf);

                        if (equal_variance) {
                            _phase = 2;
                            break;
                        } else {
                            win.shift_and_grow(f_shift, f_grow);
                            if (win.size < ms*window_start) {
                                break;
                            } else {
                                win.shift_and_reset(f_shift, window_start);
                                ms *= g_m;
                            }
                            break;
                        }
                    case 2:

                        equal_mean = t_test<double>(win0, win1, t_conf);
                        if (equal_mean) {
                            _phase = 3;
                            break;
                        } else {
                            win.shift_and_grow(t_shift, t_grow);
                           _phase = 1;
                        }

                        break;
                    case 3:
                        break;
                    default:
                        std::cout << "Error: should be unreachable\n";
                        exit(1);

                }
                std::cout << "Exiting early...\n";
                break;
            }

            //return std::nullopt;
            return std::optional<uint64_t>{10};

        }

};
            /*
            for (int i = 0; i < data_summ.size(); i++) {
                std::cout << data_summ.at(i) << ' ';
            }
            std::cout << std::endl;
            */
