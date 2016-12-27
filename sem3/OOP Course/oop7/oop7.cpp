// oop7.cpp : Defines the entry point for the console application.
//
#include "stdafx.h"
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"
#include "TQueue.h"
#include "TQueueItem.h"
#include "TList.h"

void message_print() {
	std::cout << "Hello, here are possbile actions: " << std::endl;
	std::cout << "1: Push back item. Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;
	std::cout << "2: Pop front item. Enter # of the 2nd container" << std::endl;
	std::cout << "3: Search.  Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;;
	std::cout << "4: Remove item. Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;
	std::cout << "5: Destroy all container" << std::endl;
	std::cout << "6: Output  all container items" << std::endl;
	std::cout << "q: Quit" << std::endl;
}

int _tmain(int argc, _TCHAR* argv[])
{
	int speed, cost;
	float road_clearance;
	std::string s;
	int choice = 0;
	Cars *item = nullptr;
	message_print();
	TList<TQueue, Cars> l;
	TQueue<Cars> q;
	size_t i = 0;

	while ((choice = getchar()) != 'q') {
		fflush(stdin);
		switch (choice) {
		case '1':
			fflush(stdin);
			std::cout << "Enter position to insert: ";
			std::cin >> i;
			fflush(stdin);
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				Jeep jeep(cost, road_clearance);
				l.Push(i, jeep);
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				l.Push(i, Sedan(cost, speed));
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				l.Push(i, Hatchback(cost, speed));
			}
			else std::cout << "Wrong action!" << std::endl;
				
			message_print();
			fflush(stdin);
			continue;

		case '2':
			std::cout << "Enter position to pop: ";
			std::cin >> i;
			fflush(stdin);
			l.Pop(i);
			message_print();
			continue;

		case '3':
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				if (l.Search(Jeep(cost, road_clearance)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				if (l.Search(Sedan(cost, speed)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				if (l.Search(Hatchback(cost, speed)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else std::cout << "Wrong choice!" << std::endl;
			message_print();
			fflush(stdin);
			continue;
			
		case '4':
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				l.Delete(Jeep(cost, road_clearance));
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				l.Delete(Sedan(cost, speed));
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				l.Delete(Hatchback(cost, speed));
			}
			else std::cout << "Wrong action!" << std::endl;
			message_print();
			fflush(stdin);
			continue;

		case '5':
			l.Destroy();
			message_print();
			continue;

		case '6':
			std::cout << l;
			message_print();
			continue;

		case 'q':
			break;

		default:
			std::cout << "Wrong action!" << std::endl;
			message_print();
			continue;
		}
	}
	/*Sedan sedan(1, 1);
	Jeep jeep(1, 1);
	//l.PushBack(Sedan(3400000, 210));
	//l.PushBack(new Sedan(1200000,239));
	Cars *car1 = new Sedan(2, 2);
	l.PushBack(car1);
	l.PushBack(sedan);
	l.Delete(sedan);
	q.Delete(Sedan(1000000, 10));
	std::cout << "!!!" << std::endl;

	q.PushBack(car1);
	q.PushBack(jeep);
	if (q.Search(jeep))
	std::cout << "yes!" << std::endl;
	else std::cout << "no" << std::endl;
	std::cout << q;
	q.Destroy();*/
	//std::cout << q;
	system("pause");
	return 0;
}