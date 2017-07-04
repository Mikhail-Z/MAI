#pragma once
#include <ctime>
#define INFINITY INT_MAX

using namespace std;
time_t startTime = 0, endTime = 0;

struct DGraphEdge
{
	int sourceVertex;
	int destinationVertex;
	int weight;

	DGraphEdge(int _sourceVertex, int _destinationVertex, int _weight)
	{
		sourceVertex = _sourceVertex;
		destinationVertex = _destinationVertex;
		weight = _weight;
	}
};

class DGraph
{
private:
	int verticesCount;
	int edgesCount;
	vector<DGraphEdge> edges;
	vector<int> distances;
	int sourceVertex;
	int destinationVertex;

	void ReadDataFromFile(string _fileName)
	{
		ifstream fin = ifstream(_fileName);
		int vertex1 = 0, vertex2 = 0, edgeWeight = 0;
		
		fin >> verticesCount;
		fin >> edgesCount;
		fin >> sourceVertex;
		fin >> destinationVertex;

		sourceVertex -= 1;
		destinationVertex -= 1;
	
		while (!fin.eof())
		{
			fin >> vertex1;
			fin >> vertex2;
			fin >> edgeWeight;

			vertex1 -= 1;
			vertex2 -= 1;
			
			edges.push_back(DGraphEdge(vertex1, vertex2, edgeWeight));
		}
	}

public:
	
	DGraph()
	{
		ReadDataFromFile("sample.gr");
	}

	
	string BellmanFordParallelAlgorithm()
	{
		startTime = clock();
		distances = vector<int>(verticesCount, INFINITY);
		bool end = false;

		distances[sourceVertex] = 0;

		while (!end) {
			end = true;

			//#pragma omp parallel for schedule(dynamic, 1) 
			for (int j = 0; j < edgesCount; j++)
			{
				if (distances[edges[j].sourceVertex] < INFINITY)
				{
					if (distances[edges[j].destinationVertex] > distances[edges[j].sourceVertex] + edges[j].weight)
					{																					 
						distances[edges[j].destinationVertex] = distances[edges[j].sourceVertex] + edges[j].weight;
						end = false;
					}
				}
			}
		}
		endTime = (clock() - startTime) / (double)(CLOCKS_PER_SEC / 1000);
		cout << "Ellapsed time: " << endTime << endl;
		return (distances[destinationVertex] != INFINITY) ? to_string(distances[destinationVertex]) : "No solution";
	}
};