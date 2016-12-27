#ifndef	JEEP_H
#define JEEP_H

#include <iostream>
#include "Cars.h"

class Jeep:public Cars {
public:
	Jeep();
	Jeep(int cost, float road_clearance);
	Jeep(std::istream& is1, std::istream& is2);
	Jeep(const Jeep &orig);
	double Score();
	float RoadClearance();
	int Cost();
	void Print();
	Jeep &operator=(Jeep &right);
	friend Jeep operator +(const Jeep &left, const Jeep &right);
	friend std::istream& operator>>(std::istream& is, Jeep &jeep);
	friend std::ostream& operator<<(std::ostream &os, const Jeep &obj);
    ~Jeep();

	virtual Cars* Clone() override
	{
		return new Jeep(*this);
	}

private:
	int cost;
	float road_clearance;

};

#endif JEEP_H