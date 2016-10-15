#include "stdio.h"
#include "functions.h"
#include "point.h"
#include "stdlib.h"
#include <string.h>

void print(char* filename) {
     unit u1;
     FILE *f1=fopen(filename, "rb");
     if (f1==NULL) {
         ;
     }
     while (!feof(f1)) {
          if (fread(&u1, sizeof(unit), 1, f1))
              printf("%s %s %s %d %s\n",u1.name, u1.side, u1.type, u1.cost, u1.can_attack);
     }
     fclose(f1);
}

int append(FILE *f1, unit u) {
    if (f1 == NULL) {
        return 1;
    }
    if (!fwrite(&u, sizeof(u), 1, f1)) {
        return 2;
    }
    return 0;
}

void zero(char* filename) {
   FILE *f1=fopen(filename, "wb");
   fclose(f1);
}

int TxtToBin(char* text_name, FILE* f1)
{
    FILE *in;
    unit u;
    char tmp[100];
    if ((in=fopen(text_name, "r")) != NULL)
    {
        while (!feof(in))
        {
            if (fgets(tmp, 100, in) != NULL ) {
                char* pch = strtok (tmp," ");
                int i=0;
                while (pch != EOF)
                  {
                        switch(i)
                        {
                            case 0:
                                strcpy(u.name,pch);
                                break;
                            case 1:
                                strcpy(u.side,pch);
                                break;
                            case 2:
                                strcpy(u.type,pch);
                                break;
                            case 3:
                                u.cost = atoi(pch);
                                break;
                            case 4:
                                strcpy(u.can_attack,pch);
                                break;
                        }
                        pch = strtok (NULL, " ");
                        i++;
                  }
                printf("yes\n");
                int result;
                if (result == append(f1, u)){
                    printf("yes\n");
                    return result;
                }

            }
        }
        fclose(in);
    }
    else return 3;

    return 0;
}
