#ifndef CARS_H
#define CARS_H


class Cars {
public:
    bool operator==(Cars &right);
    Cars &operator=(Cars &right);
	virtual double Score() = 0;
	virtual void Print() = 0;
	virtual ~Cars(){};
	virtual Cars* Clone() = 0;
};

#endif CARS_H