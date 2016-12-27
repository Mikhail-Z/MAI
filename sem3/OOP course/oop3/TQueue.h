#ifndef  TQUEUE_H
#define TQUEUE_H

#include <iostream>
#include "TQueueItem.h"

class TQueue {
public:
	TQueue();
	TQueue(const TQueue &orig);

	TQueue(Cars &car);
	int GetSize();
	void PushBack(Cars &car);
	void PushBack(Cars* car);
	TQueueItem* Search(Cars &car);
	Cars* PopFront();
	void Delete(Cars &car);
	bool Empty();
	void Destroy();
	friend std::ostream& operator<<(std::ostream &os, const TQueue &queue);
	
	void ISize();
	void DSize();
	
	~TQueue();
	
private:
	TQueueItem *head;
	TQueueItem *tail;

	int size;
	
};
#endif // ! TQUEUE_H


