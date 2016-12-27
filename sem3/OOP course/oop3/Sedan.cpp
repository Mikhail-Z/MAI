#include "stdafx.h"
#include <iostream>
#include "Sedan.h"

Sedan::Sedan() :Sedan(1000000, 10) {
}

Sedan::Sedan(int a, int b) : cost(a), speed(b) {
	std::cout << "Sedan created" << std::endl;
}

Sedan::Sedan(std::istream& is1, std::istream &is2) {
	is1 >> cost;
	is2 >> speed;
}

Sedan::Sedan(const Sedan &orig) {
	cost = orig.cost;
	speed = orig.speed;
	std::cout << "Sedan copy created" << std::endl;
}

int Sedan::Speed() {
	return speed;
}

int Sedan::Cost() {
	return cost;
}

void Sedan::Print() {
	std::cout << "S:" << cost << ", " << speed;
}

double Sedan::Score() {
	return cost / speed;
}

Sedan& Sedan::operator=(Sedan &right) {
	if (this == &right)
		return *this;
	(*this).cost = right.cost;
	(*this).speed = right.speed;
	std::cout << "operator =: success" << std::endl;
	return (*this);
}

Sedan operator+(const Sedan &left, const Sedan &right) {
	return Sedan(left.cost + right.cost, left.speed + right.speed);
}

std::istream &operator>>(std::istream &is, Sedan &Sedan) {
	is >> Sedan.cost;
	is >> Sedan.speed;
	return is;
}

std::ostream& operator<<(std::ostream& os, const Sedan &Sedan) {
	std::cout << Sedan.cost << ", " << Sedan.speed;
	return os;
}

Sedan::~Sedan(){
	std::cout << "Sedan deleted" << std::endl;
}