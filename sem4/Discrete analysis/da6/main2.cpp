#include <cstdlib>
#include <iomanip>
#include <cstdio>
#include <cstring>
#include "tvector.h"

const int b = 10000;

void substr(char *str,int l,int r, char *tmp) {
        strncpy(tmp, &str[l], (size_t)(r - l + 1));
        tmp[r - l + 1] = '\0';
}

int power(int a, int b) {
    int tmp = a;
    if (b == 0)
        return 1;
    else {
        for (int i = 1; i<b; i++)
            tmp*=a;
    }
    return tmp;
}

int main()
{
    char c;
    char ch[3];
    int i = 0;
    TVector v;
    TVector v2;

    char str[100001];
    int flag = 0; //чтобы не заносить ведущие нули в строку

    while (1) {
        fflush(stdin);
        while ((c = getchar()) != '\n'&& c != EOF) {
            if (c == '0' && !flag) {
                continue;
            }
            str[i] = c;

            flag = 1;
            i++;
        }
        if (c == EOF)
            break;
        if (i == 0)
            str[i++] = '0';//если все нули, то один ноль заносим
        int j = 0;
        str[i] = '\0';
        for (i = strlen(str)-1; i >= 0; i--) {
            j++;
            if (j == 4) {
                char *s = new char[j+1];
                substr(str,i,i+j-1,s);
                 //так как основани системы счисления 10 000, то двигаясь назад по 4 символа заношу в элемент вектор
                v.push_back(atoi(s));
                delete[]s;
                j = 0;
            }
        }
        if (j != 0) {//если дошли до конца, а 4 символа не набралось
            char *s = new char[j+1];
            substr(str, i+1,i+j,s);
            v.push_back(atoi(s));
            delete[]s;
            j = 0;
        }
        j = 0;
        i = 0;
        flag = 0;
        fflush(stdin);
        int l = strlen(str);
        memset(str, '\0', l);
        while ((c = getchar()) != '\n'&& c != EOF) {
            if (c == '0' && !flag) {
                continue;
            }
            str[i] = c;
            flag = 1;
            i++;
        }
        if (i == 0)
            str[i++] = '0';
        if (c == EOF)
            break;
        j = 0;
        str[i] = '\0';
        TVector res;
        for (i = strlen(str)-1; i >= 0; i--) {
            j++;
            if (j == 4) {
                char *s = new char[j+1];
                substr(str,i,i+j-1,s);
                 //так как основани системы счисления 10 000, то двигаясь назад по 4 символа заношу в элемент вектор
                v2.push_back(atoi(s));
                delete[]s;
                j = 0;
            }
        }
        if (j != 0) {
            char *s = new char[j+1];
            substr(str, i+1,i+j,s);
            v2.push_back(atoi(s));
            delete[]s;
            j = 0;
        }
        memset(str, '\0', l);
        j = 0;
        flag = 0;
        i = 0;
        fflush(stdin);
        if (c == EOF)
            break;
        fgets(ch,3,stdin);
        fflush(stdin);
        if (c == EOF)
            break;

        if (ch[0] == '+') {
            res = v + v2;
            std::cout << res;
        }
        else if (ch[0] == '-') {
            if (v < v2) {
                std::cout << "Error" << std::endl;
                v.Delete();
                v2.Delete();
                continue;
            }
            res = v - v2;
            std::cout << res;
        }
        else if (ch[0] == '*') {
            if (v2.Size() == 1)
                res = v*v2[0];
            else
                res = v*v2;
            std::cout << res;
        }
        else if (ch[0] == '^') {
            int num = 0;
            if (v.Size() == 1 && v[0] == 0) {
                if (v2.Size() == 1 && v2[0] == 0)
                    std::cout<<"Error"<<std::endl;
                else
                    std::cout<<0<<std::endl;
            }
            else if (v2.Size() == 1 && v2[0] == 0)
                std::cout<<1<<std::endl;
            else {
                for (int i = v2.Size()-1; i >= 0; i--) {
                    num += v2[i] * power(b, i);
                }
                res = v^num;
                std::cout << res;
            }
        }
        else if (ch[0] == '/') {

            if (v2.Size() == 1)
                res = v / v2[0];
            else
                res = v / v2;
        }
        else if (ch[0] == '<') {
            if (v < v2)
                std::cout << "true" << std::endl;
            else std::cout << "false" << std::endl;
        }
        else if (ch[0] == '>') {
            if (v > v2)
                std::cout << "true" << std::endl;
            else std::cout << "false" << std::endl;
        }
        else if (ch[0] == '=') {
            if (v == v2)
                std::cout << "true" << std::endl;
            else std::cout << "false" << std::endl;
        }
        else
            std::cout << "Error" << std::endl;
        v.Delete();
        v2.Delete();
    }

    v.Delete();
    v2.Delete();


    return 0;
}
