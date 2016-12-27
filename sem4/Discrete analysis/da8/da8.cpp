#include <iostream>
#include <string>
#include <math.h>

using namespace std;

void money_change(unsigned int sum, int base, int power) {
    int size = 0;
    int tmp = power;
    unsigned int *rates = new unsigned int[power];
    unsigned int a;
    unsigned int d;
    while (sum>0) {
         d = pow(base, power-1);
         if ((a = sum/d) !=0) {
             sum -= a*d;
         }
         power--;
         rates[size] = a;
         size++;
    }
    for (int i = tmp - 1; i>=size; i--)
        std::cout<<0<<std::endl;
    for (int i = size-1; i>=0; i--)
        std::cout<<rates[i]<<std::endl;

    delete[]rates;
}

int main()
{
    unsigned int sum;
    int base;
    int power;

    std::cin>>power>>base;

    cin>>sum;

    money_change(sum, base, power);

    return 0;
}

