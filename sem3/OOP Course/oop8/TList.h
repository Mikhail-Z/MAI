#ifndef TLIST_H
#define TLIST_H
#include <thread>
#include <iostream>
#include "Cars.h"
#include "TIterator.h"
#include "TQueue.h"
#include "TQueueItem.h"

template <class T>
struct TListItem;
template <class T> std::ostream& operator<<(std::ostream &os, const TListItem<T>&);

template <class T>
struct TListItem {
public:
	TListItem<T>();
	TListItem<T>(T& container);
	TListItem<T>(const TListItem<T> &orig);
	T* GetContainer() const;
	~TListItem();
	friend std::ostream& operator<< <>(std::ostream &is, const TListItem<T>& item);
	size_t GetCapacity();

	TListItem<T> *next;
	TListItem<T> *prev;
	size_t capacity;
private:
	T* container;
};

template <class T>
TListItem<T>::TListItem() : container(new T), next(nullptr), prev(nullptr), capacity(0){};


template <class T>
TListItem<T>::TListItem(const TListItem<T> &orig) :container(orig.container), next(orig.prev), prev(orig.prev), capacity(0){};

template <class T>
T* TListItem<T>::GetContainer() const {
	return container;
}

template <class T>
size_t TListItem<T>::GetCapacity() {
	return capacity;
}

template <class T>
std::ostream& operator<<(std::ostream &os, const TListItem<T>& item){
	os << *(item.GetContainer());
	return os;
}

template <class T>
TListItem<T>::~TListItem() {
	std::cout << "Container deleted" << std::endl;
}


template<template<typename> class Container, class T> class TList;
template <template <typename> class Container, class T> 
std::ostream& operator<<(std::ostream &, TList<Container, T>&);

template <class T>
void QuickSortList(TQueueItem<T>*, TQueueItem<T>*);

template<template<typename> class Container, class T>
class TList {
public:
	TList();
	TList(T& item);
	TList(const TList& orig);
	bool Push(size_t i, T& item);
	bool PopFront();
	bool PopBack();
	bool Pop(size_t i);
	TListItem<Container<T>> *Search(T& item);
	bool Delete(T& item);
	void Destroy();
	void Sort();
	friend std::ostream& operator<< <Container, T>(std::ostream& os, TList<Container, T> &list);
	~TList();
	size_t GetSize();


private:
	TListItem<Container<T>> *head;
	TListItem<Container<T>> *tail;
	size_t size;
};

template <template<typename> class Container, class T>
TList<Container, T>::TList() : head(nullptr), tail(nullptr), size(0){};

template <template<typename> class Container, class T>
TList<Container, T>::TList(const TList &orig) : head(orig.head), tail(orig.tail), size(orig.size){};

template <template<typename> class Container, class T>
TList<Container, T>::TList(T& item) {
	head = tail = TListItem<Container<T>>(item);
	size = 1;
}

template <template<typename> class Container, class T>
bool TList<Container, T>::Push(size_t i, T& item) {
	if (i > size) {
		std::cout << "Too big index" << std::endl;
		return false;
	}

	TListItem<Container<T>> *it = head;
	size_t j = 0;
	while (j < i) {
		it = it->next;
		j++;
	}

	if (!it) {
		if (!head) {
			head = new TListItem<Container<T>>;
			size++;
			tail = head;
			head->GetContainer()->PushBack(item);
			head->capacity++;
		}
		else {
			it = new TListItem<Container<T>>;
			size++;
			it->GetContainer()->PushBack(item);
			it->capacity++;
			it->next = nullptr;
			it->prev = tail;
			it->prev->next = it;
			tail = it;
		}
		return true;
	}

	if (it != nullptr) {
		if (it->GetCapacity() != 5) {
			it->GetContainer()->PushBack(item);
			it->capacity++;
		}
		else {
			while (it && it->GetCapacity() == 5)
				it = it->next;
			if (it) {
				it->GetContainer()->PushBack(item);
				it->capacity++;
			}
			else {
				it = new TListItem<Container<T>>();
				it->next = nullptr;
				it->prev = tail;
				it->prev->next = it;
				tail = it;
				size++;
				it->GetContainer()->PushBack(item);
				it->capacity++;
			}
		}
	}
	return true;
}


template <template<typename> class Container, class T>
bool TList<Container, T>::PopBack() {
	TListItem<Container<T>> *ptr = tail;
	if (!ptr) {
		return false;
	}

	if (size == 1) {
		head = tail = nullptr;
		delete ptr;
		size--;
		return true;
	}
	tail = tail->prev;
	tail->next = nullptr;
	delete ptr;
	size--;
	return true;
}

template <template<typename> class Container, class T>
bool TList<Container, T>::PopFront() {
	if (!head) {
		return false;
	}

	TListItem<Container<T>> *ptr = head;

	if (size == 1) {
		head = tail = nullptr;
		delete ptr;
		size--;
		return true;
	}
	head = head->next;
	head->prev = nullptr;
	delete ptr;
	size--;
	return true;
}

template <template <typename> class Container, class T>
bool TList<Container, T>::Pop(size_t i) {
	if (i >= size)
		return false;

	TListItem<Container<T>> *ptr = head;
	size_t j = 0;
	while (j < i) {
		ptr = ptr->next;
		j++;
	}

	if (ptr) {
		if (!ptr->GetContainer()->PopFront()) {
			ptr->GetContainer()->Destroy();
			if (ptr->prev && ptr->next) {
				ptr->prev->next = ptr->next;
				ptr->next->prev = ptr->prev;
				delete ptr;
				size--;
			}
			else if (ptr->next && !ptr->prev) {
				PopFront();
			}
			else {
				PopBack();
			}
		}
		ptr->capacity--;
		return true;
	}
	return false;
}

template <template<typename> class Container, class T>
size_t TList<Container, T>::GetSize() {
	return size;
}

template <template<typename> class Container, class T>
TListItem<Container<T>>* TList<Container, T>::Search(T& item) { 
	TListItem<Container<T>>* ptr = head;
	while (ptr != nullptr) {
		if (ptr->GetContainer()->Search(item))
			return ptr;
		ptr = ptr->next;
	}
	return nullptr;
}

template <template<typename> class Container, class T>
bool TList<Container, T>::Delete(T& item) {
	TListItem<Container<T>> *ptr = head;
	if (ptr == nullptr) {
		std::cout << "FAIL" << std::endl;
		return false;
	}

	while ((ptr = Search(item)) != nullptr) {
		std::cout << "SUCCESS" << std::endl;
		ptr->GetContainer()->Delete(item);
		ptr->capacity--;
		if (ptr->capacity == 0) {
			ptr->GetContainer()->Destroy();
			if (ptr->prev && ptr->next) {
				ptr->prev->next = ptr->next;
				ptr->next->prev = ptr->prev;
				size--;
				delete ptr;
			}
			else if (ptr->next && !ptr->prev) {
				PopFront();
			}
			else {
				PopBack();
			}
		}
	}
	return true;
}


template <template<typename> class Container, class T>
void TList<Container, T>::Sort() {
	if (!head)
		return;

	TListItem<Container<T>>* i = head; TListItem<Container<T>>* j = head->next;
	TQueueItem<T>* tmpHead = i->GetContainer()->head; TQueueItem<T>* tmpTail = i->GetContainer()->tail;
	for (; j != nullptr; i = i->next, j = i->next) {
		i->GetContainer()->tail->next = j->GetContainer()->head;
		j->GetContainer()->head->last = i->GetContainer()->tail;
		tmpTail = j->GetContainer()->tail;
	}
	QuickSortList(tmpHead, tmpTail);
	for (i = head; i != nullptr; i = i->next) {
		i->GetContainer()->head->last = nullptr;
		i->GetContainer()->tail->next = nullptr;
	}
}

template <class T>
void QuickSortList(TQueueItem<T>* left, TQueueItem<T>* right) {
	decltype(left) pStart;
	decltype(right) pCurrent;
	T* nCopyInteger;

	// сортировка окончена - выход
	if (left == right) return;

	// установка двух рабочих указателей - Start и Current
	pStart = left;
	pCurrent = pStart->next;

	// итерация по списку слева направо
	while (1)
	{
		// элемент с максимальным значением помещается в начало списка
		if (pStart->GetItem()->Cost() < pCurrent->GetItem()->Cost())
		{
			nCopyInteger = pCurrent->item;
			pCurrent->item = pStart->item;
			pStart->item = nCopyInteger;
		}

		if (pCurrent == right) break;
		pCurrent = pCurrent->next;
	}



	// переключение First и Current - максимум попадает в правый конец списка
	nCopyInteger = left->item;
	left->item = pCurrent->item;
	pCurrent->item = nCopyInteger;


	// сохранение Current
	decltype(left) pOldCurrent = pCurrent;

	// рекурсия
	pCurrent = pCurrent->last;
	if (pCurrent != NULL)
	{
		if ((left->last != pCurrent) && (pCurrent->next != left)) {
			std::thread th(QuickSortList<T>, left, pCurrent);
			th.join();
		}
	}

	pCurrent = pOldCurrent;
	pCurrent = pCurrent->next;
	if (pCurrent != NULL)
	{
		if ((pCurrent->last != right) && (right->next != pCurrent)) {
			std::thread th(QuickSortList<T>, pCurrent, right);
			th.join();
		}
	}
}

template <template<typename> class Container, class T>
std::ostream& operator<<(std::ostream &os, TList<Container, T>& list) {

	for (TListItem<Container<T>>* i = list.head; i != nullptr; i = i->next) {
		os << *i;
		os << std::endl;
	}
	return os;
}

template <template<typename> class Container, class T>
void TList<Container, T>::Destroy() {
	while (head) {
		TListItem<Container<T>> *ptr = head;
		head = head->next;
		delete ptr;
		size--;
	}
}

template <template<typename> class Container, class T>
TList<Container, T>::~TList() {
	Destroy();
}
#endif