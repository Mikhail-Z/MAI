#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _Row
{
    double _key;
    char _str[81];
} Row;


void printTable(const Row *a, const int size)
{
      int i;
      printf("   Key                     Data                   \n");
      for (i = 0; i < size; i++)
           printf("%.3lf %24s \n", a[i]._key, a[i]._str);
}

void swapRows(Row *r1, Row *r2)
{
      Row tmp;

      tmp = *r1;
      *r1 = *r2;
      *r2 = tmp;
}

int binSearch(const Row *arr, const int size, const double key)
{
    int start = 0, end = size - 1, mid;

    if (size <= 0)
          return -1;

    while (start < end)
    {
          mid = start + (end - start) / 2;

         if (arr[mid]._key == key)
                  return mid;
         else if (arr[mid]._key < key)
                  start = mid + 1;
         else
                  end = mid;
    }

    if (arr[end]._key == key)
         return end;
     return -1;
}

void sort(Row *arr, const int size)
{
     int i, j;

     for (i = 1; i < size; i++)
     {
         j = i;

         while (j > 0 && arr[j]._key < arr[j - 1]._key)
        {
              swapRows(&arr[j], &arr[j - 1]);

              j--;
        }
    }
}


void reverse(Row *arr, const int size)
{
       int i, j;

       for (i = 0, j = size - 1; i < j; i++, j--)
            swapRows(&arr[i], &arr[j]);
}


int isSorted(const Row *a, const int size)
{
     int i;

     for (i = 0; i < size - 1; i++)
            if (a[i]._key > a[i + 1]._key)
            return 0;

     return 1;
}

int main(void)
{
    int flagbreak=0;
    int N;
    int i, cnt;
    char action;
    double key;

    printf("enter the number of elements\n");
    scanf("%d",&N);
    Row* arr=(Row*)malloc(sizeof(Row)*N);
    //FILE *file = fopen("C:\Qt\Tools\QtCreator\bin\kp9\input.txt", "r");

    /*if (file == NULL)
    {
        printf("Error in opening file\n");

        return 0;
    }*/

    i = 0;

    while (i<N)
    {
        printf("enter the %d key    ",i);
        scanf("%lf ", &(arr[i]._key));
        gets(arr[i]._str);
        printf("[%lf]=%s\n",arr[i]._key, arr[i]._str);
        i++;
    }
        /*str=(char*)malloc(1);
        int l=0;
        while ((ch=getchar())!= EOF)
        {
            if (ch>='0' && ch<='9' || ch=='.') {
                str[l]=ch;
                l++;
                str=(char*)realloc(str,l+1);
                }
                else break;
        }

        if (ch==EOF) break;
        int j;
        for (j=0; j<l; i++)
        {
            if (str[j]=='.')
            arr[i]._key=atof(str[j]);
        }
        int k=0;
        while ((ch=getchar())!= EOF)
        {
            if (ch!='\n') {
                arr[i]._str[k]=ch;
                k++;
            }
            else break;
        }
        i++;
    }


        /*while (i < N &&) == 1)
        {
            fscanf(file, "%c", &ch);
        getRow(file, arr[i]._str, sizeof(arr[i]._str));

        i++;
    }

    fclose(file);*/

    cnt = i;

    while(1)
    {
        printf("Menu\n");
        printf("1) Print\n");
        printf("2) Binary search\n");
        printf("3) Sort\n");
        printf("4) Reverse\n");
        printf("5) Exit\n");
        printf("Choose the action\n");
        scanf("%c", &action);

        switch (action)
        {
            case '1':
            {
                printTable(arr, cnt);

                break;
            }

            case '2':
            {
                if (!isSorted(arr, cnt))
                    printf("Error. The table is not sorted yet\n");
                else
                {
                    printf("enter the key: ");
                    scanf("%lf", &key);

                    i = binSearch(arr, cnt, key);
                    if (i > -1)
                          printf("The string is found %s\n", arr[i]._str);
                    else
                          printf("The string with this key os not found yet\n");
                }

                break;
            }

            case '3':
            {
                 sort(arr, cnt);

                 break;
            }

            case '4':
            {
                 reverse(arr, cnt);

                 break;
            }

            case '5': {flagbreak=1; break;}

            if (flagbreak) break;
      }
   }


   return 0;
}

