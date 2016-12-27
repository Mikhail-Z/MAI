#ifndef SEDAN_H
#define SEDAN_H
#include <iostream>
#include "Cars.h"

class Sedan :public Cars {
public:
	Sedan();
	Sedan(int cost, int speed);
	Sedan(std::istream& is1, std::istream& is2);
	Sedan(const Sedan &orig);
	double Score();
	int Cost();
	int Speed();
	void Print();
	Sedan &operator=(Sedan &right);
	friend Sedan operator +(const Sedan &left, const Sedan &right);
	friend std::istream& operator>>(std::istream& is, Sedan &Sedan);
	friend std::ostream& operator<<(std::ostream &os, const Sedan &obj);
	~Sedan();

	virtual Cars* Clone() override
	{
		return new Sedan(*this);
	}

private:
	int cost;
	int speed;
};
#endif // !SEDAN_H
