#ifndef TITERATOR_H
#define TITERATOR_H

#include <memory>
#include <iostream>
#include "Cars.h"
#include "TQueueItem.h"
template <class node, class T>
class TIterator {
public:
	TIterator(node *n){ node_ptr = n; }
	T* operator*() {
		return node_ptr->GetCar();
	}
	
	T* operator->() {
		return this;
	}

	void operator++() {
	   node_ptr = node_ptr->GetNext();
	}

	TIterator operator++(int) {
		TIterator(*this);
		++(*this);
		return iter;
	}

	bool operator==(TIterator const& right) {
		return (node_ptr == right.node_ptr);
	}

	bool operator!=(TIterator const& right) {
		return !(*this == right);
	}

private:
	node *node_ptr;
};

#endif