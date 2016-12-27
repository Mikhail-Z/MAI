#include <iostream>
#include <limits>
#include <memory>


long int flag = 2147483647;

int main()
{
    int n, m;
    std::cin>>n>>m;
    int **myPath = new int*[n];
    for (int i = 0; i<n; i++)
        myPath[i] = new int[m];
    long int *lastStr = new long int[m];
    long int *curStr = new long int[m];

    for (int i = 0; i<m; i++)
        std::cin>>lastStr[i];

    for (int j = 1; j<n; j++) {
        for (int i = 0; i<m; i++) {
            std::cin>>curStr[i];
        }

        for (int i = 0; i<m; i++) {

            long int min = flag;

            if (i == 0) {
                if (lastStr[i]<min) {
                    min = lastStr[i];
                    myPath[j][i] = i;
                }
                if (lastStr[i+1]<min) {
                    min = lastStr[i+1];
                    myPath[j][i] = i+1;
                }
            }
            else if (i == m-1) {
                if (lastStr[i-1]<min) {
                    min = lastStr[i-1];
                    myPath[j][i] = i-1;
                }
                if (lastStr[i]<min) {
                    min = lastStr[i];
                    myPath[j][i] = i;
                }
            }
            else {
                if (lastStr[i-1]<min) {
                    min = lastStr[i-1];
                    myPath[j][i] = i-1;
                }

                if (lastStr[i]<min) {
                    min = lastStr[i];
                    myPath[j][i] = i;
                }

                if (lastStr[i+1]<min) {
                    min = lastStr[i+1];
                    myPath[j][i] = i+1;
                }
            }
            curStr[i] = curStr[i] + min;
        }
        for (int i = 0; i<m; i++) {
            lastStr[i] = curStr[i];
        }
    }

    long int min = lastStr[0];
    int j = 0;
    for (int i = 1; i<m; i++) {
        if (lastStr[i]<min) {
            min = lastStr[i];
            j = i;
        }
    }
    std::cout<<min<<std::endl;
    /*for (int i = 0; i<n; i++) {
        for (int j = 0; j<m; j++) {
            std::cout<<myPath[i][j]+1<<" ";
        }
        std::cout<<std::endl;
    }*/
    int last = 0;


    int *rightWay = new int[n];

    for(int i = n-1; i>0; i--) {
        if (i == n - 1) {
            last = myPath[n-1][j];
            rightWay[i] = j;
        }
        else {
            rightWay[i] = last;
            last = myPath[i][last];
        }
    }

    rightWay[0] = last;
    int i;
    for (i = 0; i<n-1; i++) {
        std::cout<<"("<<i+1<<","<<rightWay[i]+1<<") ";
    }
    std::cout<<"("<<i+1<<","<<rightWay[i]+1<<")";
    std::cout<<std::endl;

    for (int i = 0 ; i<n; i++)
        delete[]myPath[i];

    delete[]myPath;
    delete[]rightWay;
    delete[]lastStr;
    delete[]curStr;

    return 0;
}

