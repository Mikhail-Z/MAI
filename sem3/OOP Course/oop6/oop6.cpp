#include "stdafx.h"
#include "Cars.h"
#include "Jeep.h"
#include "Sedan.h"
#include "Hatchback.h"
#include "TQueue.h"
#include "TQueueItem.h"

void message_print() {
	std::cout << "Hello, here are possbile actions: " << std::endl;
	std::cout << "1: Push item.  Enter\n\t1. Jeep. Then enter price and road clearance\n\t2. Sedan. Then enter price and speed\n\t3. Hatchback. Then enter price and speed" << std::endl;
	std::cout << "2: Pop item" << std::endl;
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
	TQueue<Cars> q;
	int choice = 0;

	message_print();

	while ((choice = getchar()) != 'q') {
		fflush(stdin);
		switch (choice) {
		case '1':
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
			message_print();
			fflush(stdin);
			continue;

		case '2':
			q.PopFront();
			message_print();
			continue;

		case '3':
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
			message_print();
			fflush(stdin);
			continue;

		case '4':
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
			message_print();
			fflush(stdin);
			continue;

		case '5':
			q.Destroy();
			message_print();
			continue;

		case '6':
			std::cout << q;
			message_print();
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
