#include "stdafx.h"
#include "TQueue.h"
#include <iostream>
#include "Jeep.h"
TQueue::TQueue() :TQueue(Jeep()){ std::cout << "!!!" << std::endl; }

TQueue::TQueue(const TQueue &orig) {
	head = orig.head;
	tail = orig.tail;
	size = orig.size;
}

std::ostream& operator<<(std::ostream &os, const TQueue &queue) {
		//if (queue.size != 0) {
		TQueueItem *ptr = queue.head;
		while (ptr != nullptr) {
			os << (*ptr) << std::endl;
			ptr = ptr->GetNext();
		}
	//}
	return os;
}

TQueue::TQueue(Jeep&& jeep) {
	head = tail = new TQueueItem(jeep);
	//tail = tail->GetNext();
	size = 1;
	tail->next = nullptr;
}

void TQueue::PushBack(Jeep &&jeep) {
	/*tail = new TQueueItem(jeep);
	tail = tail->GetNext();
	size++;*/

	//TQueueItem *tmp = new TQueueItem(jeep);
	std::cout << "&&" << std::endl;
	TQueueItem *item = new TQueueItem(jeep);
	item->next = nullptr;
	tail->next = item;
	tail = item;
	size++;
}

void TQueue::PushBack(Jeep &jeep) {
	/*TQueueItem *newObj = new TQueueItem(jeep);
	tail = newObj;
	tail = tail->GetNext();
	ISize();*/
	std::cout << "&" << std::endl;
	TQueueItem *item = new TQueueItem(jeep);
	item->next = nullptr;
	tail->next = item;
	tail = item;
	size++;
}

Jeep TQueue::PopFront() {
	Jeep jeep;

	TQueueItem *tmp = head;
	if (head != nullptr)
		jeep = tmp->GetCar();
	head = head->GetNext();
	delete tmp;
	DSize();
	return jeep;
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
	delete head;
}