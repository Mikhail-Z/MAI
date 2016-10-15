#include "functions.h"

int print(char* filename) {
     country s1;
     FILE *f1=fopen(filename, "rb");
     if (f1==NULL) {
         return 1; //ошибка чтения файла
     }
     while (!feof(f1)) {
          if (fread(&s1, sizeof(country),1,f1))
              printf("%s %d %s %f\n",s1.name, s1.population, s1.capital, s1.space);
     }
     fclose(f1);
     return 0;
}

int append(char* filename, country s) {
    FILE *f1=fopen(filename, "ab");
    if (f1==NULL) {
        return 1; //ошибка доступа к файлу
    }
    if (!fwrite(&s, sizeof(s), 1, f1)) {
        return 2; //ошибка записи в файл
    }
    fclose(f1);
    return 0;
}

int TxtToBin(char* txtfilename, char* binfilename)
{
    FILE *in;
    country c;
    int s=sizeof(c);
    char mystring[100];
    if ((in=fopen(txtfilename, "r")) != NULL)
    {
        while (!feof(in)) {
        if (fgets(mystring, 100, in) != NULL ) {
            char* pch = strtok (mystring," ");
            int i=0;
            while (pch != "\0")
              {
                    switch(i)
                    {
                        case 0: strcpy(c.name,pch); break;
                        case 1: c.population = atoi(pch); break;
                        case 2: strcpy(c.capital,pch); break;
                        case 3: c.space = atoi(pch); break; // from *char to int
                    }
                    pch = strtok (NULL, " ");
                    i++;
              }
            append(binfilename, c);
        }
    }
        fclose(in);
    }
    else return 1;//ошибка открытия текстового файла

    return 0;
}
