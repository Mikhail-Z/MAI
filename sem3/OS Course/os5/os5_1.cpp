#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include "stdafx.h"
#include "Vector.h"

int _tmain(int argc, _TCHAR* argv[])
{
	int tmp;
	Vector v;
	tmp = Create(&v);
	
	tmp = Resize(&v);
	
	char enter[255];
	int i;
	for (i = 0; i < 10; i++) {
		printf(": ");
		scanf("%s", enter);
		//tmp = Push(&v, i, enter);
		Push(&v, i, enter);
		printf("%s\n", v.word[i].mystring);
	}
	Destroy(&v);
	system("Pause");
	return 0;
}
