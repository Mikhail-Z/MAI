#include "udt.h"

data_type pop_front(queue *q)
{
    data_type res;
    res=q->body[q->first];
    q->first=q->first%MAXSIZE;
    q->size--;
    return res;
}

void create(queue *q)
{
    q->size=0;
    q->first=0;
}

int is_empty(queue *q)
{
    return q->size==0;
}

void push_back(queue *q, data_type a)
{
    q->body[(q->size+q->first)%MAXSIZE]=a;
    q->size++;
}

int size(const queue *q)
{
    return q->size;
}

void print(const queue *q)
{
    int i=q->first;
    int j=0;
    while (j<q->size)
    {
        printf("%d \t", q->body[i%MAXSIZE].key);
        printf("%d \n", q->body[i%MAXSIZE].value);
        j++;
        i++;
    }
}

void insert(queue *q, data_type a) //добавление элемента в начало
{
if (q->first!=0)
{
    q->first--;
    q->body[q->first]=a;
    q->size++;
}
else
{
    q->first=MAXSIZE-1;
    q->body[q->first]=a;
    q->size++;
}
}
