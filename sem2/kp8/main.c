#include <stdio.h>
#include "List.h"


// функция из задания
// очистить список, если в нем есть элемент, равный заданному значению
void task(List* L, Type value)
{
    Iterator it = begin(*L), it_end = end(*L);
    for (; !equals(it, it_end); next(&it)) {
        if (*it.pos == value) {
            delete_list(L);
            break;
        }
    }
}



int main(void)
{
    int  i; int n; int x;
    int qbreak=0;
    printf("enter the number of elements\n");
    scanf("%d",&n);
    List L = new_list(0);
    Iterator it=begin(L);
    for (i=0; i<n; i++)
    {
        scanf("%d", &x);
        push_back(&L,x);
    }
    printf("enter the command\n");
    char *str;
    while(1)
    {
        int l;
        int n=0;
        l=0;
        str=(char*)malloc(1);
        str[l]=getchar();
        it=begin(L);
        if (str[l]=='d' || str[l]=='a' || str[l]=='t' || str[l]=='q' || str[l]=='p')
        switch(str[l])
        {
            case 'a':
            {
                int y,z;
                printf("enter the position  and the value to insert\n");
                scanf("%d   %d\n",&y,&z);
                for (i = 0; i < y; ++i) {
                  next(&it);
                 }
                insert(&L, it, z);
                break;
             }

        case 'd':
        {
            printf("enter the position for delete(<=size) \n");
            int pos;
            scanf("%d", &pos);
            it.pos += pos;
            erase(&L, it);
            break;
        }
        case 't':
        {
            printf("enter value, if this value is in list the list will be deleted\n");
            scanf("%d",&n);
            task(&L, n);

            break;
        }

        case 'p':
        {
            print(L);
            break;
        }
        case 'q':
        {
            qbreak=1;
            break;
        }
    }
    if (qbreak==1) {printf("Press enter for exit"); break;}
}
    return 0;
}

