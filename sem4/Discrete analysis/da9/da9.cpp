#include <iostream>
#include <stdbool.h>

using namespace std;

struct edge {
    int begin;
    int end;
    int weight;
};

int main()
{
    const long long INF = static_cast<long long>(1) << 60;
    int n, m,start,finish;
    cin>>n>>m>>start>>finish;
    long int *d = new long int[n+1];
    edge *graph = new edge[m+1];
    int b,e,w;
    for (int i = 1; i <= m; i++) {
        cin>>b>>e>>w;
        graph[i].begin = b;
        graph[i].end = e;
        graph[i].weight = w;
    }

    bool isChange = 0;
    for (int i = 1; i<=n; i++) {
        d[i] = INF;
    }
    d[start] = 0;

    for (;;) {
        for (int i = 1; i <= m; i++) {
            if (d[graph[i].begin]!=INF) {
                if (d[graph[i].end] > d[graph[i].begin] + graph[i].weight) {
                    isChange = 1;
                    d[graph[i].end] = d[graph[i].begin] + graph[i].weight;
                }
            }
        }
        if (isChange == 0)
            break;
        else isChange = 0;
    }
    if (d[finish] == INF)
	cout<<"No solution"<<endl;
    else
        cout<<d[finish]<<endl;
    delete[]d;
    delete[]graph;
    return 0;
}
