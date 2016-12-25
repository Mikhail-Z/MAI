#ifndef	JEEP_H
#define JEEP_H

#include <iostream>

class Jeep {
public:
	Jeep();
	Jeep(int cost, float road_clearance);
	Jeep(const Jeep &orig);
	double Score();
	friend Jeep operator +(const Jeep &left, const Jeep &right);
	Jeep &operator =(const Jeep &orig);
	friend std::ostream& operator<<(std::ostream &os, const Jeep &obj);
	virtual ~Jeep();

private:
	int cost;
	float road_clearance;

};

#endif JEEP_H