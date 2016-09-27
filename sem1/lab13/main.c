#include <stdio.h>
#include <ctype.h>
#define VOWELS (1u<<('a'-'a') | 1u<<('e'-'a') | 1u<<('i'-'a') | 1u<<('o'-'a') | 1u<<('u'-'a'))

unsigned int char_to_set(char c) {
    c=tolower(c);
    return 1u<<(c-'a');
}


int main(void)
{   printf("vowels = %x\n", VOWELS);

    int slovo=0,flag=0;
    char c;

    unsigned int letters_set =0;

    while ((c = getchar())!=EOF) {
        //printf("c= %d",c);
        if (c>='a' && c<='z' || c>='A' && c<='Z') {
             letters_set=letters_set | char_to_set(c);  //накапливание текста
        //printf("letters_set %x\n", letters_set);
        }
        else if (c=='\n' || c=='\t' || c==' ' || c==',') {
            //printf("letters_set %x\n", letters_set);
            letters_set = letters_set & VOWELS;  //Слово закончилось. Идет побитовая коньюнкция с маской гласных
            while (letters_set != 0) {
            if (letters_set & 1) flag+=1; //анализ каждой буквы слова справа налево
            //printf("flag = %d\n ",flag);
            letters_set = letters_set>>1;//
            }
            if (flag==1) slovo+=1;
            flag=0;
            letters_set=0;
        }


    }
    if (slovo>0) printf("est kak minimum odno slovo s odnoi glasnoy %d",slovo
                        );
    else printf("net slov s odnoi glasnoy");
    return 0;
}

