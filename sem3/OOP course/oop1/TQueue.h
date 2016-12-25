#ifndef  TQUEUE_H
#define TQUEUE_H

#include <iostream>
#include "Jeep.h"
#include "TQueueItem.h"

class TQueue {
public:
	TQueue();
	TQueue(const TQueue &orig);

	TQueue(Jeep &&jeep);
	int GetSize();
	void PushBack(Jeep &&jeep);
	void PushBack(Jeep &jeep);
	Jeep PopFront();
	bool Empty();
    friend std::ostream& operator<<(std::ostream &os,const TQueue &queue);
	
	void ISize();
	void DSize();
	
	~TQueue();
	
private:
	TQueueItem *head;
	TQueueItem *tail;

	int size;
	
};
#endif // ! TQUEUE_H


