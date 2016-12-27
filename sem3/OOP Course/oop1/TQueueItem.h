#ifndef TQUEUEITEM_H
#define TQUEUEITEM_H

#include "Jeep.h"
class TQueueItem {
public:
	//TQueueItem();
	TQueueItem(const Jeep& Jeep);
	TQueueItem(const TQueueItem& orig);
	friend std::ostream& operator<<(std::ostream& os, const TQueueItem& obj);
	
	TQueueItem *GetNext();
	Jeep GetCar() const;
	~TQueueItem();
	TQueueItem *next;
private:
	
	Jeep jeep;
};

#endif