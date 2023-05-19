#include <vector>
#include <iostream>
#include <functional>
#include <numeric>
#include <optional>

#include <boost/math/distributions/fisher_f.hpp>
#include <boost/math/distributions/students_t.hpp>
#include <boost/math/statistics/linear_regression.hpp>
#include <boost/iterator/counting_iterator.hpp>
using boost::math::fisher_f;
using boost::math::students_t;
using boost::math::statistics::simple_ordinary_least_squares;

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



    std::cout << "F-test\n";
    std::cout << "  sd1: " << sd1 << std::endl;
    std::cout << "  sd2: " << sd2 << std::endl;
    std::cout << "  N1: " << N1 << std::endl;
    std::cout << "  N2: " << N2 << std::endl;
    std::cout << "  F: " << F << std::endl;
    std::cout << "  ucv2: " << ucv2 << std::endl;
    std::cout << "  lcv2: " << lcv2 << std::endl;

    // If true, don't reject, meaning variances are equal
    return ! ((ucv2 < F) || (lcv2 > F));
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

public:
    uint64_t start;
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
        bool debug        = true;
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

        std::optional<std::pair<uint64_t, uint64_t>> run(std::vector<uint64_t> data) {
            uint64_t new_len = data.size() / summarize;
            std::vector<double> data_summ(new_len);
            for (uint64_t i = 0; i < new_len; i++) {
                data_summ[i] = std::accumulate(data.begin()+(i  )*summarize, data.begin()+(i+1)*summarize, 0, std::plus<uint64_t>()) / summarize;
            }

            Window<double> win(data_summ, 0, window_start);

            WinRange<double> win0 = std::nullopt;
            WinRange<double> win1 = std::nullopt;
            WinRange<double> win_combo = std::nullopt;
            uint64_t ms = ms_init;
            int _phase = 1;
            bool equal_variance = false;
            bool equal_mean = false;
            std::vector<double> slope_history;
            std::vector<double> xs, ys;
            uint64_t combo_len;
            double intercept, coeff;
            std::pair<double, double> ols_ret;
            WinPoint<double> pt_ret;
            uint64_t x_star;
            double y_hat, y_true;
            uint32_t pos, neg;

            while (true) {
                switch (_phase) {
                    case 1: //F-test

                        if (debug) std::cout << "Entering phase 1\n";

                        win0 = win.get(0);
                        win1 = win.get(1);

                        if (!win1) {
                            std::cout << "Phase 1: Couldn't get window!\n";
                            return std::nullopt;
                        }

                        if (debug) std::cout << "Phase 1: Testing variance\n";
                        equal_variance = f_test<double>(win0, win1, f_conf);

                        if (equal_variance) {
                            if (debug) std::cout << "Phase 1: Variance equal\n";
                            _phase = 2;
                        } else {
                            if (debug) std::cout << "Phase 1: Variance not equal\n";
                            win.shift_and_grow(f_shift, f_grow);
                            if (win.size < ms*window_start) {

                            } else {
                                win.shift_and_reset(f_shift, window_start);
                                ms *= g_m;
                            }
                        }
                        break;

                    case 2: // T-test
                        if (debug) std::cout << "Entering phase 2\n";

                        equal_mean = t_test<double>(win0, win1, t_conf);
                        if (equal_mean) {
                            _phase = 3;
                        } else {
                            win.shift_and_grow(t_shift, t_grow);
                           _phase = 1;
                        }
                       break;

                    case 3: // Projection Test
                        if (debug) std::cout << "Entering phase 3\n";
                        slope_history.clear();

                        for (int j = 0; j < p_j; j++){
                            win_combo = win.get_range(0+j, 1+j);
                            if (!win_combo) {
                                std::cout << "FtPjRG: Never converged!\n";
                                return std::nullopt;
                            }

                            combo_len = std::distance(std::get<0>(*win_combo), std::get<1>(*win_combo));
                            xs = std::vector<double>(boost::counting_iterator<double>(0), boost::counting_iterator<double>(combo_len));
                            ys = std::vector<double>(std::get<0>(*win_combo), std::get<1>(*win_combo));

                            //ref: https://www.boost.org/doc/libs/master/libs/math/doc/html/math_toolkit/linear_regression.html
                            ols_ret = simple_ordinary_least_squares(xs, ys);
                            intercept = std::get<0>(ols_ret);
                            coeff = std::get<1>(ols_ret);

                            pt_ret = win.get_point(proj_dist);
                            if (!pt_ret) {
                                std::cout << "FtPjRG: Never converged!\n";
                                return std::nullopt;
                            }
                            x_star = std::get<0>(*pt_ret);
                            y_true = std::get<1>(*pt_ret);

                            y_hat = intercept + coeff * x_star;

                            if (abs(y_hat - y_true) > proj_delta) {
                                win.shift_and_grow(p_shift, p_grow);
                                _phase = 1;
                                break;
                            }

                            slope_history.push_back(coeff);

                        }
                        pos = 0;
                        neg = 0;
                        if (p_j > 2) {
                            for (auto x : slope_history) {
                                pos += x > 0;
                                neg += x < 0;
                            }

                            if (pos && neg) {
                                return std::optional<std::pair<uint64_t,uint64_t>>{std::make_pair(win.start,win.size*2)};
                            } else {
                                _phase = 1;
                                break;
                            }
                        }

                        return std::optional<std::pair<uint64_t,uint64_t>>{std::make_pair(win.start,win.size*2)};
                        break; //unreachable
                    default:
                        std::cout << "Error: should be unreachable\n";
                        exit(1);

                }
            }

            //return std::nullopt;
            return std::optional<std::pair<uint64_t,uint64_t>>{std::make_pair(10,10)};

        }

};
            /*
            for (int i = 0; i < data_summ.size(); i++) {
                std::cout << data_summ.at(i) << ' ';
            }
            std::cout << std::endl;
            */
