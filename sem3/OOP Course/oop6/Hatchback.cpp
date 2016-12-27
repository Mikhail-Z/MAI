#include "stdafx.h"
#include <iostream>
#include "Hatchback.h"

Hatchback::Hatchback() :Hatchback(800000, 9.2) {

}

Hatchback::Hatchback(int a, float b) : cost(a), speed(b) {
	std::cout << "Hatchback created" << std::endl;
}

Hatchback::Hatchback(std::istream& is1, std::istream &is2) {
	is1 >> cost;
	is2 >> speed;
}

Hatchback::Hatchback(const Hatchback &orig) {
	cost = orig.cost;
	speed = orig.speed;
	std::cout << "Hatchback copy created" << std::endl;
}

int Hatchback::Speed() {
	return speed;
}

int Hatchback::Cost() {
	return cost;
}

void Hatchback::Print() {
	std::cout << "H:" << cost << ", " << speed<<" ";
}

double Hatchback::Score() {
	return cost / speed;
}

Hatchback& Hatchback::operator=(Hatchback &right) {
	if (this == &right)
		return *this;
	(*this).cost = right.cost;
	(*this).speed = right.speed;
	std::cout << "operator =: success" << std::endl;
	return (*this);
}

Hatchback operator+(const Hatchback &left, const Hatchback &right) {
	return Hatchback(left.cost + right.cost, left.speed + right.speed);
}

std::istream &operator>>(std::istream &is, Hatchback &Hatchback) {
	is >> Hatchback.cost;
	is >> Hatchback.speed;
	return is;
}

std::ostream& operator<<(std::ostream& os,  Hatchback &Hatchback) {
	std::cout << Hatchback.cost << ", " << Hatchback.speed;
	return os;
}

Hatchback::~Hatchback(){
	std::cout << "Hatchback deleted" << std::endl;
}