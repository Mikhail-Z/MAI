#ifndef  TQUEUE_H
#define TQUEUE_H

#include <iostream>
#include "TQueueItem.h"
#include "TIterator.h"
template<class T>
class TQueue;

template <class T>
std::ostream& operator<<(std::ostream &, TQueue<T> &);


template <class T> class TQueue {
public:
	TQueue();
	TQueue(const TQueue &orig);

	TQueue(T &item);
	int GetSize();
	void PushBack(T &item);
	void PushBack(T* item);
	TQueueItem<T>* Search(T &item);
	bool PopFront();
	bool Delete(T &item);
	bool Empty();
	void Destroy();
	friend std::ostream& operator<< <>(std::ostream &os, TQueue<T> &queue);
		
	~TQueue();

	TIterator<TQueueItem<T>, T> begin();
	TIterator<TQueueItem<T>, T> end();
	
//private:
	TQueueItem<T> *head;
	TQueueItem<T> *tail;

	int size;
	
};

template <class T>
TQueue<T>::TQueue() :head(nullptr), tail(nullptr), size(0){ }

template <class T>
TQueue<T>::TQueue(const TQueue &orig) {
	head = orig.head;
	tail = orig.tail;
	size = orig.size;
}

template <class T>
TQueue<T>::TQueue(T &item) {
	head = tail = new TQueueItem(item);
	item.Print();
	head->GetItem()->Print();
	size = 1;
	tail->next = nullptr;
}

template <class T>
TIterator<TQueueItem<T>, T> TQueue<T>::begin() {
	return TIterator<TQueueItem<T>, T>(head);
}

template <class T>
TIterator<TQueueItem<T>, T> TQueue<T>::end() {
	return TIterator<TQueueItem<T>, T>(nullptr);
}

template <class T>
std::ostream& operator<<(std::ostream &os, TQueue<T> &queue) {
	//if (queue.size != 0) {
	/*std::cout << "in print" << std::endl;
	TQueueItem<T> *ptr = queue.head;
	while (ptr != nullptr) {
		os << *ptr << std::endl;	
		ptr = ptr->GetNext();
	}
	std::cout << "size=" << queue.size << std::endl;
	//}*/

	if (queue.head == nullptr) {
		os << "Queue is empty, size: ";
		os << queue.size << std::endl;
	}
	else {
		for (auto i : queue) {
			(*i).Print();
			os << " ";
		}
	}
	return os;
}

template <class T>
TQueueItem<T>* TQueue<T>::Search(T &item) {
	TQueueItem<T>* ptr = head;
	while (ptr != nullptr) {
		if (*((*ptr).GetItem()) == item)
			return ptr;
		else ptr->GetItem()->Print();
		ptr = ptr->next;
	}
	return nullptr;
}

template <class T>
void TQueue<T>::PushBack(T &item) {

	if (head == nullptr) {
		head = tail = new TQueueItem<T>(item);
		size = 1;
		tail->next = nullptr;
		tail->last = nullptr;
		head->last = nullptr;
		head->next = nullptr;
		return;
	}
	else {
		TQueueItem<T> *it = new TQueueItem<T>(item);
		it->next = nullptr;
		it->last = tail;
		tail->next = it;
		tail = it;
	}
	size++;
}

template <class T>
void TQueue<T>::PushBack(T* item) {
	if (head == nullptr) {
		head = tail = item;
		size = 1;
		tail->next = nullptr;
		tail->last = nullptr;
		head->last = nullptr;
		head->next = nullptr;
		return;
	}
	else {
		it = item;
		it->next = nullptr;
		it->last = tail;
		tail->next = it;
		tail = it;
	}
	size++;
}

template <class T>
bool TQueue<T>::PopFront() {
	if (size == 0) {
		std::cout << "No itens in queue. Size: " << size << std::endl;
		return false;
	}
	if (size == 1) {
		T* item = nullptr;
		TQueueItem<T>* tmp = head;
		item = head->GetItem();
		head = tail = nullptr;
		size--;
		item->Print();
		std::cout << std::endl;
		delete tmp;
		std::cout << "Size: " << size << std::endl;
		return false;
	}

	T* item = nullptr;
	TQueueItem<T> *tmp = head;
	//if (head != nullptr)
	item = head->GetItem();
	head = head->next;
	head->last = nullptr;
	item->Print();
	std::cout << std::endl;
	delete tmp;
	size--;
	std::cout << "Size: " << size << std::endl;
	return true;
}

template <class T>
bool TQueue<T>::Delete(T &item) {
	TQueueItem<T> *ptr = head;
	if (ptr == nullptr) {
		std::cout << "FAIL" << std::endl;
		return false;
	}

	if ((ptr = Search(item)) != nullptr) {
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
		return true;
	}
	else std::cout << "FAIL" << std::endl;
	return false;
}

template <class T>
void TQueue<T>::Destroy() {
	while (head) {
		TQueueItem<T> *ptr = head;
		head = head->next;
		//head->last = nullptr;
		delete ptr;
		size--;
	}
	tail = head = nullptr;
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


