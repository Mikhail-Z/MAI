#ifndef TEXTITARATOR_H
#define TEXTITERATOR_H

template <template<typename> class Container, class T>
class TExtIterator {
public:
	TExtIterator(Container<T>* p) :ptr(p){};
	Container<T>* operator*() {
		return ptr->GetContainer();
	}

	Container<T>* operator->() {
		return this;
	}

	void operator++() {
		ptr = prtr->next;
	}

	TExtIterator operator++(int) {
		TExtIterator(*this);
		++(*this);
		return iter;
	}

	bool operator==(const TExtIterator &right) {
		return (ptr == right->ptr);
	}

	bool operator!=(const TExtIterator &right) {
		return !(ptr == right->ptr);
	}
private:
	Container<T>* ptr;
};

#endif 