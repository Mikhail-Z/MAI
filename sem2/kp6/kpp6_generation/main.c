#include <stdio.h>
#include <string.h>
#include "functions.h"
#include "point.h"
#include <stdlib.h>

void usage()
{
    printf("Usage: program <input text file> <output binary file> [-f] \n");
}

int main(int argc, char* argv[])
{
    int flag_f=0;
    char* bin_name;
    char* text_name;
    if (argc < 3){
        usage();
        return 1;
    }
    else{
        text_name = argv[1];
        bin_name = argv[2];
        int i;
        for (i = 3; i < argc; i++) {
            if (strcmp(argv[i],"-f") == 0)
                flag_f=1;
        }
    }
    zero(bin_name);
    FILE *f1=fopen(bin_name, "ab");
    int result=TxtToBin(text_name, f1);
    fclose(f1);
    if (flag_f)
    {
        print(bin_name);
    }
    return 0;
}

