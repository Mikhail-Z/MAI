#include <stdio.h>
#include "udt.h"
#include "sort.h"



int main() {

   // переменную-очередь
   queue q;
   //create(&q);
   int n;
   //Заполнить очередь данными
   printf("enter the number of elements (less than 20)\n");
   scanf("%d",n);
   int i;
   printf("enter the key and additional number for every number\n");
   for (i=0; i<n; i++)
   scanf("%d \t %d",q.body[i].key, q.body[i].value);
   //Распечатать содержимое очереди
   print(&q);

   //Отсортировать очередь
   int count = 0;
   while(count < size(&q)) {
       count = 0;
       sort_insert(&q, &count);
   }

   //Распечатать новое содержимое очереди
   print(&q);


}

/*void swap(int *a[i],int *a[i+1])
{
    int tmp;
    tmp=a[i];
    a[i]=a[i+1];
    a[i+1]=tmp;
}

int main(void)
{
    int n;
    int x[n];
    int i;
    int j;
    for (i=1; i<n; i++)
        for (j=i; j>0 && x[j-1]>x[j]; j--)
            swap(x[j-1], x[j]);
}

*/
