#include "stdafx.h"
#include "TQueueItem.h"
#include "Cars.h"
#include "Hatchback.h"
#include "Sedan.h"
#include "Jeep.h"
#include <iostream>

TQueueItem::TQueueItem() : car(nullptr), next(nullptr), last(nullptr){}


TQueueItem::TQueueItem(Cars &cars):car(&cars),next(nullptr) {
	std::cout << "Queue item: created" << std::endl;
}

TQueueItem::TQueueItem(TQueueItem& orig) {
	car = orig.car;
	next = orig.next;
}

Cars *TQueueItem::GetCar() const {
	return this->car;
}

TQueueItem* TQueueItem::GetNext() {
	return this->next;
}

std::ostream &operator<<(std::ostream& os, const TQueueItem &obj) {
	os << "[";
	
	obj.GetCar()->Print();
	os<< "] ";
	return os;
}

TQueueItem::~TQueueItem() {
	std::cout << "Queue item: deleted" << std::endl;
}