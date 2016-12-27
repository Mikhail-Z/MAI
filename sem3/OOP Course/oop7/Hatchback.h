#ifndef HATCHBACK_H
#define HATCHBACK_H
#include "Cars.h"
class Hatchback :public Cars {
public:
	Hatchback();
	Hatchback(int cost, float road_clearance);
	Hatchback(std::istream& is1, std::istream& is2);
	Hatchback(const Hatchback &orig);
	double Score();
	int Cost();
	int Speed();
	void Print();
	Hatchback &operator=(Hatchback &right);
	friend Hatchback operator +(const Hatchback &left, const Hatchback &right);
	friend std::istream& operator>>(std::istream& is, Hatchback &Hatchback);
	friend std::ostream& operator<<(std::ostream &os, Hatchback &obj);
     ~Hatchback();

	 virtual Cars* Clone() override
	 {
		 return new Hatchback(*this);
	 }

private:
	int cost;
	int speed;

};
#endif // !HATCHBACK_H
