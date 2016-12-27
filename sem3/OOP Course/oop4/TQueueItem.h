#ifndef TQUEUEITEM_H
#define TQUEUEITEM_H
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"

template <class T> class TQueueItem;
template <class T> std::ostream& operator<<(std::ostream &, const TQueueItem<T> &);

template <class T>
class TQueueItem {
public:
	TQueueItem();
	TQueueItem(T& car);
	TQueueItem(TQueueItem& orig);
	friend std::ostream& operator<< <>(std::ostream& os, const TQueueItem<T>& obj);
	
	TQueueItem<T> *GetNext();
	T *GetCar() const ;
	~TQueueItem();
	TQueueItem<T> *next;
	TQueueItem<T> *last;

private:
	T *car;
};

template <class T>
TQueueItem<T>::TQueueItem() : car(nullptr), next(nullptr), last(nullptr){}

template <class T>
TQueueItem<T>::TQueueItem(T &cars) : car(cars.Clone()), next(nullptr) {
	std::cout << "Queue item: created" << std::endl;
}
template <class T>
TQueueItem<T>::TQueueItem(TQueueItem& orig) {
	car = orig.car;
	next = orig.next;
}

template <class T>
T *TQueueItem<T>::GetCar() const {
	return this->car;
}

template <class T>
TQueueItem<T>* TQueueItem<T>::GetNext() {
	return this->next;
}

template <class T>
std::ostream &operator<< (std::ostream& os, const TQueueItem<T> &obj) {
	os << "[";

	obj.GetCar()->Print();
	os << "] ";
	return os;
}

template <class T>
TQueueItem<T>::~TQueueItem() {
	std::cout << "Queue item: deleted" << std::endl;
}
#endif