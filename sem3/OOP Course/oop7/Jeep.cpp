#include "stdafx.h"
#include "Jeep.h"

Jeep::Jeep() :Jeep(1200000, 18.6) {

}

Jeep::Jeep(int a, float b) : cost(a), road_clearance(b) {
	std::cout << "Jeep created" << std::endl;
}

Jeep::Jeep(std::istream& is1, std::istream &is2) {
	is1 >> cost;
	is2 >> road_clearance;
}

Jeep::Jeep(const Jeep &orig) {
	cost = orig.cost;
	road_clearance = orig.road_clearance;
	std::cout << "Jeep copy created" << std::endl;
}

float Jeep::RoadClearance() {
	return road_clearance;
}

int Jeep::Cost() {
	return cost;
}

void Jeep::Print() {
	std::cout << "J:" << cost << ", " << road_clearance << " ";
}

double Jeep::Score() {
	return cost / road_clearance;
}

Jeep& Jeep::operator=(Jeep &right) {
	if (this == &right)
		return *this;
	(*this).cost = right.cost;
	(*this).road_clearance = right.road_clearance;
	return (*this);
}

Jeep operator+(const Jeep &left, const Jeep &right) {
	return Jeep(left.cost + right.cost, left.road_clearance + right.road_clearance);
}

std::istream &operator>>(std::istream &is, Jeep &jeep) {
	is >> jeep.cost;
	is >> jeep.road_clearance;
	return is;
}

std::ostream& operator<<(std::ostream& os, Jeep &jeep) {
	std::cout << jeep.cost << ", " << jeep.road_clearance;
	return os;
}

Jeep::~Jeep(){
	std::cout << "Jeep deleted" << std::endl;
};