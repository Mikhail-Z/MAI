#ifndef  TQUEUE_H
#define TQUEUE_H

#include <iostream>
#include "TQueueItem.h"

template<class T>
class TQueue;

template <class T>
std::ostream& operator<<(std::ostream &, const TQueue<T> &);


template <class T> class TQueue {
public:
	TQueue();
	TQueue(const TQueue &orig);

	TQueue(T &car);
	int GetSize();
	void PushBack(T &car);
	void PushBack(T* car);
	TQueueItem<T>* Search(T &car);
	T* PopFront();
	void Delete(T &car);
	bool Empty();
	void Destroy();
	friend std::ostream& operator<< <>(std::ostream &os, const TQueue<T> &queue);
		
	~TQueue();
	
private:
	TQueueItem<T> *head;
	TQueueItem<T> *tail;

	int size;
	
};

template <class T>
TQueue<T>::TQueue() :head(nullptr), tail(nullptr), size(0){ /*head = tail;*/ }

template <class T>
TQueue<T>::TQueue(const TQueue &orig) {
	head = orig.head;
	tail = orig.tail;
	size = orig.size;
}

template <class T>
TQueue<T>::TQueue(T &car) {
	head = tail = new TQueueItem(car);
	car.Print();
	head->GetCar()->Print();
	size = 1;
	tail->next = nullptr;
}

template <class T>
std::ostream& operator<<(std::ostream &os, const TQueue<T> &queue) {
	std::cout << "in print" << std::endl;
	TQueueItem<T> *ptr = queue.head;
	while (ptr != nullptr) {
		os << *ptr << std::endl;	
		ptr = ptr->GetNext();
	}
	std::cout << "size=" << queue.size << std::endl;
	//}
	return os;
}

template <class T>
TQueueItem<T>* TQueue<T>::Search(T &car) {
	TQueueItem<T>* ptr = head;
	while (ptr != nullptr) {
		if (*((*ptr).GetCar()) == car)
			return ptr;
		else ptr->GetCar()->Print();
		ptr = ptr->next;
	}
	return nullptr;
}

template <class T>
void TQueue<T>::PushBack(T &car) {

	if (head == nullptr) {
		head = tail = new TQueueItem<T>(car);
		size = 1;
		tail->next = nullptr;
		tail->last = nullptr;
		head->last = nullptr;
		head->next = nullptr;
		return;
	}
	else {
		TQueueItem<T> *item = new TQueueItem<T>(car);
		item->next = nullptr;
		item->last = tail;
		tail->next = item;
		tail = item;
	}
	size++;
}

template <class T>
void TQueue<T>::PushBack(T* car) {
	if (head == nullptr) {
		head = tail = new TQueueItem<T>(*car);
		size = 1;
		tail->next = nullptr;
		tail->last = nullptr;
		head->last = nullptr;
		head->next = nullptr;
		return;
	}
	else {
		TQueueItem<T> *item = new TQueueItem<T>(*car);
		item->next = nullptr;
		item->last = tail;
		tail->next = item;
		tail = item;
	}
	size++;
}

template <class T>
T* TQueue<T>::PopFront() {
	if (size == 0)
		return nullptr;

	if (size == 1) {
		T* car = nullptr;
		TQueueItem<T>* tmp = head;
		car = head->GetCar();
		head = tail = nullptr;
		size--;
		return car;
	}

    T* car = nullptr;
	TQueueItem<T> *tmp = head;
	car = head->GetCar();
	head = head->next;
	head->last = nullptr;
	std::cout << "here" << std::endl;
	size--;
	return car;
}

template <class T>
void TQueue<T>::Delete(T &car) {
	TQueueItem<T> *ptr = head;
	if (ptr == nullptr) {
		std::cout << "FAIL" << std::endl;
		return;
	}

	if ((ptr = Search(car)) != nullptr) {
		TQueueItem<T> *tmp_ptr = ptr;
		if (ptr->last != nullptr && ptr->next != nullptr) {
			ptr->last->next = ptr->next;
			ptr->next->last = ptr->last;
			delete tmp_ptr;
		}
		else if (ptr->next == nullptr && ptr->last != nullptr) {
			ptr->last->next = ptr->next;
			ptr = ptr->last;
			tail = ptr;
			delete tmp_ptr;
		}
		else if (ptr->next != nullptr && ptr->last == nullptr) {
			ptr = ptr->next;
			ptr->last = nullptr;
			head = ptr;
			delete tmp_ptr;
		}
		else {
			head = tail = nullptr;
			delete ptr;
		}
		size--;
		std::cout << "SUCCESS" << std::endl;
	}
	else std::cout << "FAIL" << std::endl;
}

template <class T>
void TQueue<T>::Destroy() {
	while (head) {
		TQueueItem<T> *ptr = head;
		head = head->next;
		delete ptr;
		size--;
	}
}

template <class T>
int TQueue<T>::GetSize() {
	return size;
}

template <class T>
bool TQueue<T>::Empty() {
	return (head == nullptr);
}

template <class T>
TQueue<T>::~TQueue() {
	Destroy();
}
#endif // ! TQUEUE_H


