// oop3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"
#include "TQueue.h"
#include "TQueueItem.h"

int _tmain(int argc, _TCHAR* argv[])
{
	int speed = 0, cost = 0;
	float road_clearance = 0;
	std::cout << "Enter cost and speed" << std::endl;
	std::cin >> cost, std::cin >> speed;
	Sedan sedan;
	TQueue q;
	Cars *jeep = (new Jeep(12000000, 34.3));
	q.PushBack(Sedan(cost,speed));
	std::cout << q;
	
	q.PushBack(sedan);
	q.Delete(sedan);
	std::cout << q;
	q.Delete(sedan);
	std::cout << q;
	q.PushBack(sedan);
	std::cout << q;
	if (q.Search(sedan))
		std::cout << "yes!" << std::endl;
	else std::cout << "no" << std::endl;
	q.Delete(sedan);
	std::cout << q;
	system("pause");
	return 0;
}

