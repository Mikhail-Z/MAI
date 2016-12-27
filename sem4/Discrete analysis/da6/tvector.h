#ifndef TVECTOR_H
#define TVECTOR_H
#include <string>
#include <iostream>
#include <stdbool.h>
    class TVector {//ewde
    public:
        TVector();
        TVector(int size);
        ~TVector();
        TVector(const TVector &v); //конструктор копирования

        void push_back(int n);//положить в крнец вектора
        void pop_back();//из конца убрать элемент, тем самым уменьшив размер
        void resize(int cap);//изменить вместимость (capacity)
        int Size() const;//вернуть размер
        int last();//вернуть последний элемент
        int Capacity() const;
        void Delete();
        bool Empty();
        int &operator[](int i);

        void push(int i, int x);
        void repair();
        TVector& operator=(const TVector &v2);

        friend bool operator == (TVector &v, TVector &v2);
        friend bool operator <(TVector &v, TVector &v2);
        friend bool operator >(TVector &v, TVector &v2);


        friend void copyToLess(TVector v, int r, int l,TVector *res);
        friend void copyToBigger(TVector v, int r, int l, TVector *res);
        friend void minus(TVector v, TVector v2,TVector *res);
        friend void division(TVector v, TVector v2, TVector *res);
	friend void zeroing(TVector *v);

        friend TVector operator + (TVector v, TVector v2);
        friend TVector operator - (TVector v, TVector v2);
        friend TVector operator * (TVector v, int num);
        friend TVector operator * (TVector v, TVector v2);
        friend TVector operator / (TVector v, TVector v2);
        friend TVector operator / (TVector v, int num);
        friend TVector operator ^ (TVector v, int num);

        friend std::ostream& operator<<(std::ostream& os, TVector& v);

        void reverse(); //реверс вектора

    private:
        int *numbers;
	int size;
        int capacity;

    };



#endif // TVECTOR_H

