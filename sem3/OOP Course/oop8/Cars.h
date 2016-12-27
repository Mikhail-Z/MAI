#ifndef CARS_H
#define CARS_H

#include <iostream>
class Cars {
public:
    bool operator==(Cars &right);
    Cars &operator=(Cars &right);
	virtual int Cost() = 0;
	virtual double Score() = 0;
	virtual void Print() = 0;
	virtual ~Cars(){};
	virtual Cars* Clone() = 0;
	friend std::ostream& operator<<(std::ostream &, Cars&);
};

#endif CARS_H