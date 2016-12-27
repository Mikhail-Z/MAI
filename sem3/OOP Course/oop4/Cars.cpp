#include "stdafx.h"
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"


Cars &Cars::operator=(Cars &right) {
	std::cout << "Here" << std::endl;
	if (dynamic_cast<Jeep*>(this) != nullptr && dynamic_cast<Jeep*>(&right) != nullptr) {
		std::cout << "Here" << std::endl;
		return *dynamic_cast<Jeep*>(this) = *dynamic_cast<Jeep*>(&right);
	}

	if (dynamic_cast<Sedan*>(this) != nullptr && dynamic_cast<Sedan*>(&right) != nullptr)
		return *dynamic_cast<Sedan*>(this) = *dynamic_cast<Sedan*>(&right);

	if (dynamic_cast<Hatchback*>(this) != nullptr && dynamic_cast<Hatchback*>(&right) != nullptr)
		return *dynamic_cast<Hatchback*>(this) = *dynamic_cast<Hatchback*>(&right);

}

bool Cars::operator==( Cars &right) {
	if (dynamic_cast<Jeep*>(this) != nullptr && dynamic_cast<Jeep*>(&right) != nullptr) {
		Jeep *a = dynamic_cast<Jeep*>(this);
		Jeep *b = dynamic_cast<Jeep*>(&right);
		return a->Cost() == b->Cost() && a->RoadClearance() == b->RoadClearance();
	}
	
	if (dynamic_cast<Sedan*>(this) != nullptr && dynamic_cast<Sedan*>(&right) != nullptr) {
		Sedan *a = dynamic_cast<Sedan*>(this);
		Sedan *b = dynamic_cast<Sedan*>(&right);
		return a->Cost() == b->Cost() && a->Speed() == b->Speed();
	}

	if (dynamic_cast<Hatchback*>(this) != nullptr && dynamic_cast<Hatchback*>(&right) != nullptr) {
		Hatchback *a = dynamic_cast<Hatchback*>(this);
		Hatchback *b = dynamic_cast<Hatchback*>(&right);
		return a->Cost() == b->Cost() && a->Speed() == b->Speed();
	}
	return false;
}