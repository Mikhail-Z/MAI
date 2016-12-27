#ifndef TQUEUEITEM_H
#define TQUEUEITEM_H
#include <memory>
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"
#include "TIterator.h"

template <class T> class TQueueItem;
template <class T> std::ostream& operator<<(std::ostream &, const TQueueItem<T> &);

template <class T>
class TQueueItem {
public:
	TQueueItem();
	TQueueItem(T& item);
	TQueueItem(TQueueItem<T>& orig);
	friend std::ostream& operator<< <>(std::ostream& os, const TQueueItem<T>& obj);
	
	TQueueItem<T> *GetNext();
	T* GetItem() const;
	~TQueueItem();
	TQueueItem<T> *next;
	TQueueItem<T> *last;
	/*void* operator new(size_t size);
	void operator delete(void *ptr);*/

//private:
	T *item;
};

template <class T>
TQueueItem<T>::TQueueItem() : item(nullptr), next(nullptr), last(nullptr){}

template <class T>
TQueueItem<T>::TQueueItem(T &item) : item(item.Clone()), next(nullptr), last(nullptr) {
	//this->item = &item;
	//this->item = item;
	//this->next = nullptr;
	std::cout << "Queue item: created" << std::endl;
}
template <class T>
TQueueItem<T>::TQueueItem(TQueueItem& orig) {
	item = orig.item;
	next = orig.next;
	last = orig.last;
}

template <class T>
T *TQueueItem<T>::GetItem() const{
	return this->item;
}

template <class T>
TQueueItem<T>* TQueueItem<T>::GetNext(){
	return this->next;
}

template <class T>
std::ostream &operator<< (std::ostream& os, const TQueueItem<T> &obj) {
	os << "[";

	obj.Getitem()->Print();
	os << "] ";
	return os;
}

template <class T>
TQueueItem<T>::~TQueueItem() {
	std::cout << "Queue item: deleted" << std::endl;
}

/*template <class T>
void* TQueueItem<T>::operator new(size_t size){
	std::cout << "Allocated: " << size << std::endl;
	return malloc(size);
}

template <class T>
void TQueueItem<T>::operator delete(void* ptr) {
	std::cout << "Deleted" << std::endl;
	free(ptr);
}*/
#endif