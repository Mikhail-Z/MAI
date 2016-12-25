// oop1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Jeep.h"
#include "TQueue.h"
#include "TQueueItem.h"

int _tmain(int argc, _TCHAR* argv[])
{
	TQueue q;
	std::cout << q;
	Jeep jeep1, jeep2,jeep3;
	jeep1 = jeep2 + jeep3;
	q.PushBack(jeep1);
	std::cout << q;

	std::cout << q;
	//std::endl;
	std::cout << "here" << std::endl;
	Jeep j;
	j = q.PopFront();
	j = q.PopFront();
	std::cout << q;
	system("pause");

	return 0;
}

