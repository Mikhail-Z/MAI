#include <iostream>
#include <exception>
#include <new>
#include <iomanip>
#include <cstdlib>
#include "tvector.h"

const int b = 10000; //основание системы счисления


TVector::TVector() {
    numbers = new int[8]();
    size = 0;
    capacity = 8;
    //std::cout << "I am alive!" << std::endl;
}

TVector::TVector(int newsize) {
    try {
        numbers = new int[newsize]();
    }
    catch (std::bad_alloc &e) {
        std::cout<< "Error" << std::endl;
        std::exit(1);
    }
    size = 0;
    capacity = newsize;

}

TVector::~TVector() {
    //std::cout << "I am die!" << std::endl;
    delete[]numbers;
    size = 0;
    capacity = 0;
}

TVector::TVector(const TVector &v) :size(v.size),capacity(v.capacity){
    try { numbers = new int[v.Capacity()](); }
    catch (std::bad_alloc &e) {
        //std::cerr << "Bad alloc: " << e.what() << std::endl;
        std::cout<<"Error"<<std::endl;
    }
    for (int i = 0; i < v.Size(); i++) {
        numbers[i] = v.numbers[i];
    }
}

void TVector::resize(int newcap) {
    capacity = newcap;
    try {
        int* temp = new int[newcap]();
        for (int i = 0; i < size; i++)
            temp[i] = numbers[i];

        delete [] numbers;
        numbers = temp;
    }
    catch (std::bad_alloc &e) {
        //std::cerr << "Bad alloc caught:" << e.what() << std::endl;
        std::cout<<"Error"<<std::endl;
        std::exit(1);
    }
}

void TVector::push_back(int n) {
    if (capacity == size + 1) {
        resize(capacity * 2);
    }
    numbers[size] = n;
    size++;
}
void TVector::repair() {
    int i = capacity-1;
    while (i>=0 && numbers[i] == 0){
        i--;
    }
    size = i+1;
}

void TVector::push(int i, int x) {
    if (i < capacity) {
        numbers[i] = x;
    }
    if (i>=size)
        repair();
}

void TVector::pop_back() {
    size--;
}

bool TVector::Empty() {
    return size == 0;
}

int TVector::Size() const {
    return size;
}

int TVector::Capacity() const {
    return capacity;
}

int TVector::last() {
    return numbers[size - 1];
}
void TVector::Delete() {
    try {
        delete[] numbers;
        numbers = new int[8]();
    }
    catch(std::bad_alloc& e) {
       // std::cerr << "Bad alloc caught:" << e.what() << std::endl;
        std::cout<<"Error"<<std::endl;
        std::exit(1);
    }
    size = 0;
    capacity = 8;
}

void TVector::reverse() {
    try {
        int* temp = new int[capacity]();
        for (int i = 0; i < size; i++)
            temp[i] = numbers[size-i-1];

        delete[] numbers;
        numbers = temp;
    }
    catch (std::bad_alloc &e) {
        //std::cerr << "Bad alloc caught:" << e.what() << std::endl;
        std::cout<<"Error"<<std::endl;
        std::exit(1);
    }
}


int max(int x, int y) {
    return x > y ? x : y;
}

int ost(int a, int d) {
    if (d == 0)
        return 0;
    if ((a >= 0 && d > 0) || (a <= 0 && d < 0))
        return a % d;
    else
        return (abs(a / d) + 1)*d - abs(a);
}

void zeroing(TVector *v) {
    for (int i = 0; i<v->Size(); i++)
        v->numbers[i] = 0;
    v->size = 0;
}

void copyToLess(TVector v, int r, int l,TVector *res) {
    for (int j = 0; j + r <=l; j++)
        (*res).push_back(v[j + r]);
}

void copyToBigger(TVector v, int r,int l,TVector *res) {
    for (int j = 0; j + r <=l; j++)
        (*res).numbers[j + r] = v[j];
}

void minus(TVector v, TVector v2, TVector *res) {
    if (v < v2) {
        (*res) = v2 - v;
        (*res).push_back(-1);
    }
    else
        (*res) = v - v2;
}

TVector operator + (TVector v, TVector v2) {
    int k = 0;
    int i;
    int x, y;
    TVector res(max(v.Size(), v2.Size()) + 1);
    for (i = 0; i < max(v.Size(),v2.Size()); i++) {
        x = (i < v.Size() ? v[i] : 0);
        y = (i < v2.Size() ? v2[i] : 0);

        res.push_back((x + y + k) % b);
        k = (x + y + k) / b;
    }
    if (k != 0)
        res.push_back(k);
    return res;
}

TVector operator - (TVector v, TVector v2) {

    TVector res(v.Size());
    int k = 0;

    int x, y;
    for (int i = 0; i < v.Size(); i++) {

        x = v[i];
        y = (i<v2.Size() ? v2[i] : 0);
        res.push_back(ost(x - y + k, b));
        k = x - y + k < 0 ? -1 : 0;
    }
    res.repair();
    if (res.Empty())
        res.push_back(0);
    return res;
}

TVector operator * (TVector v, int num) {
    int i, temp, k = 0;
    TVector res;

    for (i = 0; i < v.Size(); i++) {
        temp = v[i] * num + k;
        k = temp / b;
        res.push_back(temp - k*b);
    }

    if (k) {
        res.push_back(k);
    }
    return res;
}

TVector operator * (TVector v, TVector v2) {
    TVector tmp(v.Size() + v2.Size()); //создание нового вектора для записи туда ответа с последующим копированием из него в свой вектор
    for (int j = 0; j < v2.Size(); j++) {
        if (v2[j] != 0) {
            int k = 0;
            int t;
            int i;
            for (i = 0; i < v.Size(); i++) {
                t = v[i] * v2[j] + tmp[i + j] + k;
                tmp.push(i + j, t % b);
                k = t / b;
            }
            if (k > 0)
                tmp.push(j + v.Size(), k);
        }
    }
    if (tmp.Empty())
        tmp.push_back(0);
    return tmp;
}

TVector operator ^ (TVector v, int num) {
    if (num > 0)
    {
        if (v.Size() == 1 && v[0] == 0) {
            zeroing(&v);
            v.push_back(0);
            return v;
        }
        if (num % 2 == 0) {
            TVector temp = v ^ (num / 2);
            v = temp*temp;
        }
        else
            v = v * (v ^ (num - 1));
    }
    else {
        zeroing(&v);
        v.push_back(1);
    }
    return v;
}

TVector operator / (TVector v, int num) {
    TVector res(v.Size());
    int i, temp, r = 0;

    try {
        for (i = v.Size() - 1; i >= 0; i--) {
            temp = r*b + v[i];
            if (num == 0)
                throw 18;
            res.numbers[i] = temp / num;
            r = temp - res[i] * num;
        }
    }
    catch (int error) {
        std::cout<<"Error"<<std::endl;
        return res;
    }
    res.repair();
    if (res.Empty())
        res.push_back(0);
    std::cout<<res;
    return res;
}

TVector operator / (TVector v, TVector v2) {

    int d = b / (v2.last() + 1);

    int n = v2.Size();
    int m = v.Size() - v2.Size();

    if (d > 1) {
        v = v*d;
        v2 = v2 * d;
    }

    int new_q, new_r;

    if (m>0)
        v.resize(n+m+1);

     TVector res(max(m+1,8));

    for (int j = m; j >= 0; j--) {        
        new_q = (v[j + n] * b + v[j + n - 1]) / v2[n-1];
        new_r = (v[j + n] * b + v[j + n - 1]) % v2[n-1];
        while (new_r < b && (new_q == b || (new_q*v2[n - 2] > b*new_r + v[j + n - 2]))) {
            new_q -= 1;
            new_r += v2[n-1];
        }
        TVector tmp;
        copyToLess(v, j, j+n,&tmp);
        minus(tmp, v2*new_q, &tmp);
        copyToBigger(tmp, j,j+n, &v);
        res.numbers[j] = new_q;
        if (tmp.last() < 0) {
            tmp.pop_back();
            res.numbers[j] -= 1;
            v2.push_back(0);
            tmp = v2 - v;
            copyToBigger(tmp, j,j+n, &v);
            v2.pop_back();
        }
        tmp.Delete();
    }
    res.repair();
    if (res.Empty())
        res.push_back(0);
    std::cout<<res;
    return res;
}

int& TVector::operator[](int i) {
    return numbers[i];
}

TVector& TVector::operator=(const TVector& v2) {
    if (&v2 != this) {
        try {
            delete[] numbers;
            size = v2.Size();
            capacity = v2.capacity;
            numbers = new int[capacity]();
            for (int i = 0; i < size; i++)
                numbers[i] = v2.numbers[i];
        }
        catch (std::bad_alloc &e) {
            //std::cerr << "Bad alloc caught:" << e.what()<<std::endl;
            std::cout<<"Error"<<std::endl;
            std::exit(1);
        }
    }
    return *this;
}

std::ostream& operator<<(std::ostream& os, TVector& v)
{
    const size_t width = 4;
    const char fill = '0';
    for (int i = v.Size() - 1; i >= 0; i--) {
        if(i!=v.Size()-1)
            std::cout << std::setw(width) << std::setfill(fill);
        os << v[i];
    }
    std::cout<<std::endl;
    return os;
}

bool operator ==(TVector &v, TVector &v2) {
    if (v.Size() != v2.Size()) {
        return false;
    }
    else {
        for (int i = 0; i < v.Size(); i++) {
            if (v[i] < v2[i]) {
                return false;
            }
            else if(v[i] > v2[i])
                return false;
        }
        return true;
    }
}

bool operator <(TVector &v, TVector &v2) {
    if (v.Size() < v2.Size()) {
        return true;
    }
    else if (v.Size() > v2.Size())
        return false;
    else {
        for (int i = v.Size() - 1; i>=0; i--) {
            if (v[i] > v2[i])
                return false;
            else if(v[i] < v2[i])
                return true;
        }
        return false;
    }
}

bool operator >(TVector &v, TVector &v2) {
    if (v.Size() > v2.Size())
        return true;
    else if (v.Size() < v2.Size())
        return false;
    else {
        for (int i = v.Size()-1; i >= 0; i--) {
            if (v[i] > v2[i])
                return true;
            else if (v[i] < v2[i])
                return false;
        }
        return false;
    }
}
