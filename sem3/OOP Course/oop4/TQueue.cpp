#include "stdafx.h"
#include "TQueue.h"
#include <iostream>
#include "Cars.h"
#include "Jeep.h"
#include "Hatchback.h"
#include "Sedan.h"

TQueue::TQueue() :head(nullptr), tail(nullptr), size(0){ /*head = tail;*/ }

TQueue::TQueue(const TQueue &orig) {
	head = orig.head;
	tail = orig.tail;
	size = orig.size;
}

TQueue::TQueue(Cars &car) {
	head = tail = new TQueueItem(car);
	//tail = tail->GetNext();
	car.Print();
	head->GetCar()->Print();
	size = 1;
	tail->next = nullptr;
}


std::ostream& operator<<(std::ostream &os, const TQueue &queue) {
	//if (queue.size != 0) {
	std::cout << "in print" << std::endl;
	TQueueItem *ptr = queue.head;
	while (ptr != nullptr) {
		os << *ptr << std::endl;	
		ptr = ptr->GetNext();
	}
	std::cout << "size=" << queue.size << std::endl;
	//}
	return os;
}
void TQueue::PushBack(Cars &car) {

	if (size == 0) {
		head = tail = new TQueueItem(car);
		size = 1;
		tail->next = nullptr;
		head->last = nullptr;
		return;
	}
	TQueueItem* item = new TQueueItem(car);
	item->next = nullptr;
	item->last = tail;
	tail->next = item;
	tail = item;
	tail->GetCar()->Print();
	size++;
}

void TQueue::PushBack(Cars* car) {
	if (size == 0) {
		head = tail = new TQueueItem(*car);
		size = 1;
		tail->next = nullptr;
		head->last = nullptr;
		return;
	}

	TQueueItem *item = new TQueueItem(*car);
	item->next = nullptr;
	item->last = tail;
	tail->next = item;
	tail = item;
	tail->GetCar()->Print();

	size++;
}


Cars* TQueue::PopFront() {
	if (size == 0)
		return nullptr;

	if (size == 1) {
		static Cars* car = nullptr;
		TQueueItem* tmp = head;
		car = tmp->GetCar();
		head = tail = nullptr;
		return car;
	}

	static Cars* car = nullptr;
	TQueueItem *tmp = head;
	//if (head != nullptr)
	car = tmp->GetCar();
	head = head->next;
	head->last = nullptr;
	std::cout << "here" << std::endl;

	delete tmp;
	DSize();

	return car;
}

TQueueItem* TQueue::Search(Cars &car) {
	TQueueItem* ptr = head;
	while (ptr != nullptr) {
		if (*((*ptr).GetCar()) == car)
			return ptr;
		ptr = ptr->next;
	}
	return nullptr;
}

void TQueue::Destroy() {
	
	while (head) {
		TQueueItem *ptr = head;
		std::cout << 116 << std::endl;
		head = head->next;
		//head->last = nullptr;
		std::cout << 119 << std::endl;
		delete ptr;
		size--;
	}
}

void TQueue::Delete(Cars &car) {
	if (size == 0)
		return;
	TQueueItem *ptr = head;

	if (size == 1) {
		if (*((*ptr).GetCar()) == car) {
			head = tail = nullptr;
			std::cout << "SUCCESS" << std::endl;
			size--;
			return;
		}
		std::cout << "FAIL" << std::endl;
		return;
	}
	if ((ptr = Search(car)) != nullptr) {
		if (ptr->last != nullptr)
			ptr->last->next = ptr->next;
		else head = head->next;
		delete ptr;
		size--;
		std::cout << "SUCCESS" << std::endl;
	}
	else std::cout << "FAIL" << std::endl;


}

int TQueue::GetSize() {
	return size;
}

void TQueue::ISize() {
	size++;
}

void TQueue::DSize() {
	if (size>0)
		size--;
}

bool TQueue::Empty() {
	return (head == nullptr);
}

TQueue::~TQueue() {
	Destroy();
}