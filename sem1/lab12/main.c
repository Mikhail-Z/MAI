#include <stdio.h>
#include <math.h>

int mod(int m, int n)
{   int t;
    if (m<0 && n>0 || n<0 && m>0) {
        t=m/n;
        t=abs(m)-abs(t*n);
    }
    else t=m-(m/n)*n;
    if (m==0 && n>0) t=n;
    return t;
}

int main(void)
{
    int ost,n,k,odin,noll;
    printf("vvedite chislo\n");
    scanf("%d",&n);
    noll=0; odin=0;
    k=n;
    if (n==0) printf("neravnoe kolichestvo nulei i ediniz");
    else if (n>0) {
        printf("point1\n");
        while (n>0) {
            ost = n%2;
            if (ost==0) noll+=1;
            else if (ost==1) odin+=1;
            printf("%d null %d odin %d  ost %d\n",n, noll, odin, ost);
            n=n/2;


        }
        noll=noll + (sizeof(int)*8-(noll+odin));
    }
    else if (n<0) {
        printf("point3\n");
        n=-n;
        int flag=0;
        while (n>0) {
              //зная, что будет инвертирование битов, считаю кол-во наоборот.
                        //Так как потом будет прибавляться единица, возможно замещение
                       //полученных единиц нулями до первого нуля, который станет единицей. Пока этого не произошло flag=0
            ost = mod(n,2);

            if (ost==0 && flag == 0)
                noll+=1;
            else if (ost==0 && flag == 1)
                odin+=1;
            else if (ost==1 && flag == 0) {
                odin+=1;
                flag = 1;
            }
            else if (ost==1 && flag == 1)
                noll+=1;
             printf("%d null %d odin %d  ost %d\n",n, noll, odin, ost);

            n=n/2;
        }

        odin=odin + (sizeof(int)*8-(noll+odin));
    }
    printf("n=%d noll=%d odin=%d\n",n,noll,odin);
    if (k!=0 && noll==odin) printf("odinakovoe kolichestvo nulei i ediniz");
    else if (k!=0 && noll!=odin) printf("neravnoe kolichestvo nulei i ediniz");
    return 0;
}

