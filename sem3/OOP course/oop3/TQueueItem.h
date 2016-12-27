#ifndef TQUEUEITEM_H
#define TQUEUEITEM_H
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"

class TQueueItem {
public:
	TQueueItem();
	TQueueItem(Cars& car);
	TQueueItem(TQueueItem& orig);
	friend std::ostream& operator<<(std::ostream& os, const TQueueItem& obj);
	
	TQueueItem *GetNext();
	Cars *GetCar() const ;
	~TQueueItem();
	TQueueItem *next;
	TQueueItem *last;

private:
	Cars *car;
};

#endif