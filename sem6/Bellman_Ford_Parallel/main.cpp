#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <climits>
#include <omp.h>
#include <conio.h>
#include <windows.h>
#include "graph.h"
#include <cmath>
#include <ctime>
using namespace std;

int main()
{
	DGraph graph = DGraph();
	
	cout << "Parallel algorithm:" << endl;
	cout << "Result: " << graph.BellmanFordParallelAlgorithm() << endl;
	_getch();

    return 0;
}