#include "stdafx.h"
#include <string>
#include <iostream>
#include "TAllocationBlock.h"

TAllocationBlock::TAllocationBlock(size_t size, int count) : _size(size), _count(count){
	_free_count = 0;
	_used_blocks = (char*)malloc(_size * _count);
	_free_blocks = new AllocNode(_used_blocks);
	for (size_t i = 1; i < _count; i++) {
		_free_blocks[i] = new AllocNode(_used_blocks + i*_size);
		_free_blocks[i - 1].next = &_free_blocks[i];
	}
	_free_count = _count;
	std::cout << "AllocationBlock: Memory init" << std::endl;
}

void* TAllocationBlock::Allocate() {
	void *result = nullptr;
	try {
		if (_free_count > 0) {
			result = _free_blocks[_free_count-1].ptr;
			_free_count--;
			std::cout << "AllocationBlock: Allocate " << (_count - _free_count) << " of " << _count << std::endl;
		}
		else throw "Not enough memory!";
	}
	catch (std::string s) {
		std::cout << s << std::endl;
	}

	return result;
}

void TAllocationBlock::Deallocate(void *ptr) {
	std::cout << "TAllocationBlock: Deallocate block " << std::endl;
	if (_free_blocks != nullptr) {
		_free_blocks[_free_count].ptr = ptr;
		_free_count++;
		std::cout << "AllocationBlock: Allocate " << (_count - _free_count) << " of " << _count << std::endl;
	}
}

bool TAllocationBlock::HasFreeBlocks() {
	return _free_blocks > 0;
}

TAllocationBlock::~TAllocationBlock() {
	delete _used_blocks;
	AllocNode *ptr = head;
	while (head != nullptr){
		ptr = head;
		head = head->next;
		delete ptr;
	}
}


AllocNode* TAllocationBlock::GetElemBefore(AllocNode *p) {
	AllocNode* ptr = head;
	if (ptr == nullptr)
		return nullptr;
	else if (head == p)
		return head;

	while (ptr->next != nullptr && ptr->next != p)
		ptr = ptr->next;
	return ptr;
}

AllocNode* TAllocationBlock::Insert(AllocNode *p, void* k) {
	while (p != nullptr)
		p = p->next;
	return p = new AllocNode(k);
}

void TAllocationBlock::Remove(AllocNode *prev_p, AllocNode *p, void *k) {
	AllocNode *tmp_ptr = prev_p;
	if (p != nullptr && p->ptr != k) {
		tmp_ptr = p;
		p = p->next;
	}
	if (p == head) {
		tmp_ptr = p;
		p = p->next;
		head = p;
		delete tmp_ptr;
		return;
	}
	else {
		prev_p = p->next;
		p->next = nullptr;
		delete p;
		return;
	}
}

AllocNode &TAllocationBlock::operator[](size_t i) {
	try {
		if (i < 0)
			throw i;
	}
	catch (int i) {
		std::cout << "Out of Range error (index: " << i << ")" << std::endl;
		std::exit(1);
	}

	AllocNode *ptr = head;
	size_t j = 0;
	try {
		while (j < i && ptr != nullptr) {
			j++;
			ptr = ptr->next;
		}
		if (j == i && ptr != nullptr)
			return *ptr;
		else throw j;
	}
	catch (int j) {
		std::cout << "Out of range error (last possible index: " << j << std::endl;
		std::exit(2);
	}
}