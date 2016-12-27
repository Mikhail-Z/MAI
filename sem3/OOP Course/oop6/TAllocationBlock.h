#ifndef TALLOCATIONBLOCK_H
#define TALLOCATIONBLOCK_H

struct AllocNode {
	AllocNode *next;
	void *ptr;
	AllocNode(void*p) :ptr(p), next(nullptr){}
};

#include <cstdlib>
class TAllocationBlock {
public:
	TAllocationBlock(size_t size, int count);
	void* Allocate();
	void Deallocate(void* ptr);
	bool HasFreeBlocks();
	AllocNode *Insert(AllocNode *p, void *k);
	void Remove(AllocNode *prev_p, AllocNode *p, void *k);
	AllocNode& operator[](size_t i);
	AllocNode *GetElemBefore(AllocNode *p);
	virtual ~TAllocationBlock();

private:
	size_t _size;
	char *_used_blocks;
	AllocNode *_free_blocks;
	AllocNode *head;
	size_t _count;
	size_t _free_count;
};

#endif