#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "List.h"

List new_list(int size)
{
	List L;
    L.size = 0;
	L.data = malloc(size * sizeof(Type));
	return L;
}

void delete_list(List* L)
{
	free(L->data);
	L->size = 0;
}

Iterator begin(List L)
{
	Iterator it;
	it.pos = L.data;
	return it;
}

Iterator end(List L)
{
	Iterator it;
	it.pos = L.data + L.size;
	return it;
}

void next(Iterator* it)
{
	++it->pos;
}

int equals(Iterator it1, Iterator it2)
{
	return it1.pos == it2.pos;
}

void print(List L)
{
	printf("[");
	if (L.size) {
		printf("%d", L.data[0]);
        int i;
        for (i = 1; i < L.size; ++i) {
			printf(", %d", L.data[i]);
		}
	}
	printf("]\n");
}

int size(List L)
{
	return L.size;
}

Iterator insert(List* L, Iterator it, Type value)
{
	Type* new_data = malloc((L->size + 1) * sizeof(Type));
	int count = it.pos - L->data;
	memcpy(new_data, L->data, count * sizeof(Type));
	new_data[count] = value;
	memcpy(new_data + count + 1, L->data + count, (L->size - count) * sizeof(Type));
	free(L->data);
	L->data = new_data;
	++L->size;
	it.pos = L->data + count + 1;
	return it;
}


void push_back(List* L, Type value)
{
	insert(L, end(*L), value);
}

Iterator erase(List* L, Iterator it)
{
	if (L->size == 0) {
		return end(*L);
	}
    realloc(L->data, L->size*2*sizeof(int));
    Type* new_data = malloc((L->size - 1) * sizeof(Type));
	int count = it.pos - L->data;

	memcpy(new_data, L->data, count * sizeof(Type));
    memcpy(new_data + count, L->data + count + 1, (L->size - count-1) * sizeof(Type));
	free(L->data);
	L->data = new_data;
	--L->size;
	it.pos = L->data + count + 1;
	return it;
}
