#include "stdafx.h"
#include "TQueueItem.h"
#include <iostream>

//TQueueItem::TQueueItem() : TQueueItem(Jeep()){}

TQueueItem::TQueueItem(const Jeep &jeep) {
	this->jeep = jeep;
	this->next = nullptr;
	std::cout << "Queue item: created" << std::endl;
}

TQueueItem::TQueueItem(const TQueueItem& orig) {
	jeep = orig.jeep;
	next = orig.next;
}

Jeep TQueueItem::GetCar() const {
	return this->jeep;
}

TQueueItem* TQueueItem::GetNext() {
	return this->next;
}

std::ostream &operator<<(std::ostream& os, const TQueueItem &obj) {
	os << "[" << obj.jeep << "],";
	return os;
}

TQueueItem::~TQueueItem() {
	std::cout << "Queue item: deleted" << std::endl;
}