#include "sort.h"

void sort_insert(queue* q, int* count)
{
    (*count)++;
    if ((*count) < size)
    {
        data_type v1=pop_front(q);
        data_type v2=pop_front(q);
        if (v1.key > v2.key)
        {
            insert(q,v1);
            insert(q,v2);
        }
        else
        {
            insert(q,v2);
            sort_insert(q,count);
            data_type v=pop_front(q);
            if (v.key>v1.key)
            {
                insert(q,v);    //как мне кажется, это должно для быстродействия выполняться 1 раз, так как в дальнейшем будут сравниваться ключи, которые до этого были отсортированы
                insert(q,v1);   //то есть, как я понимаю, сюда встает элемент, который был неупорядочен, то есть v, а после этого его затрагивать не будем, поэтому дальнешие манипуляции по этой ветке не нужны
            }                 //нужно ли как-нибудь break сделать, как думаете?
            else if (v.key < v1.key)
            {
                insert(q,v1);
                insert(q,v);
            }
        }
    }
}
