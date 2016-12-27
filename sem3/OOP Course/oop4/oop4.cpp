// oop4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


#include "stdafx.h"
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"
#include "TQueue.h"
#include "TQueueItem.h"

int _tmain(int argc, _TCHAR* argv[])
{
	int speed, cost;
	float road_clearance;
	std::string s;
	TQueue<Cars> q;
	int choice = 0;
	Cars *item;
	std::cout << "Hello, here are possbile actions: " << std::endl;
	std::cout << "1: Push item (Press a).  Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;
	std::cout << "2: Pop item (Press p)" << std::endl;
	std::cout << "3: Search (Press s).  Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;;
	std::cout << "4: Remove item (Press r). Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;
	std::cout << "5: Destroy all container (Press d)" << std::endl;
	std::cout << "6: Output  all container items (Press o)" << std::endl;
	std::cout << "6: Quit (Press q)" << std::endl;
	
	while ((choice = getchar()) != 'q') {
		fflush(stdin);
		switch (choice) {
			std::cout << choice << std::endl;
		case 'a':
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				Jeep jeep(cost, road_clearance);
				q.PushBack(jeep);
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				q.PushBack(Sedan(cost, speed));
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				q.PushBack(Hatchback(cost, speed));
			}
			else std::cout << "Wrong action!" << std::endl;
			fflush(stdin);
			continue;

		case 'p':
			item = q.PopFront();
			std::cout << "jfkhjfk" << std::endl;
			if (item == nullptr)
				std::cout << "No remaining elements!" << std::endl;
			else  {
				item->Print();
			}
			continue;

		case 's':
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				if (q.Search(Jeep(cost, road_clearance)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				if (q.Search(Sedan(cost, speed)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				if (q.Search(Hatchback(cost, speed)) != nullptr)
					std::cout << "Yes!" << std::endl;
				else std::cout << "No!" << std::endl;
			}
			else std::cout << "Wrong choice!" << std::endl;
			fflush(stdin);
			continue;

		case 'r':
			if ((choice = getchar()) == '1') {
				std::cin >> cost >> road_clearance;
				q.Delete(Jeep(cost, road_clearance));
			}
			else if (choice == '2') {
				std::cin >> cost >> speed;
				q.Delete(Sedan(cost, speed));
			}
			else if (choice == '3') {
				std::cin >> cost >> speed;
				q.Delete(Hatchback(cost, speed));
			}
			else std::cout << "Wrong action!" << std::endl;
			fflush(stdin);
			continue;

		case 'd':
			q.Destroy();
			continue;

		case 'o':
			std::cout << q;
			continue;

		case 'q':
			break;

		default:
			std::cout << "Wrong action!" << std::endl;
			continue;
		}
	}

	system("pause");
	return 0;
}
