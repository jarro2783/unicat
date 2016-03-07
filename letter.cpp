#include <algorithm>
#include <chrono>
#include <iostream>
#include <iterator>
#include <utility>
#include "uniclass.h"

class InRange
{
    public:
    bool
    operator()(char32_t c, const std::pair<int, int>& r)
    {
        return c < r.first;
    }

    bool
    operator()(const std::pair<int, int>& r, char32_t c)
    {
        return c > r.second;
    }
};

bool
is_letter(char32_t c)
{
    //return std::binary_search(L,
    //    L + (sizeof(L) / sizeof(L[0])),
    //    c,
    //    InRange());
    return uniclass::is(c, uniclass::categories::L);
}

int main(int argc, char** argv)
{
    std::vector<char32_t> cs;
    std::vector<bool> result;
    for (char32_t c = U'¡'; c != U'ÿ'; ++c)
    {
        cs.push_back(c);
    }

    auto start = std::chrono::high_resolution_clock::now();
    for (auto c : cs)
    {
        result.push_back(is_letter(c));
    }
    auto end = std::chrono::high_resolution_clock::now();

    std::cout << std::boolalpha;
    std::copy(result.begin(), result.end(), std::ostream_iterator<bool>(std::cout, ", "));

    std::cout << std::endl <<
        std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
        << std::endl;

    return 0;
}
