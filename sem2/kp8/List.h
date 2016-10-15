#ifndef LIST_H
#define LIST_H

typedef int Type;


typedef
struct List
{
    Type*	data;
    int		size;
} List;

typedef
struct Iterator
{
    Type* pos;
} Iterator;


            List new_list(int size);

            void delete_list(List* L);

            Iterator begin(List L);

            Iterator end(List L);

            void next(Iterator* it);

            int equals(Iterator it1, Iterator it2);

            void print(List L);

            int size(List L);

            Iterator insert(List* L, Iterator pos, Type value);

            void push_back(List* L, Type value);

            Iterator erase(List* L, Iterator pos);
#endif
