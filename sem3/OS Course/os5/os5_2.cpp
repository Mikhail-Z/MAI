#include "stdafx.h"
#include "Vector.h"
#include <Windows.h>
#include "stdio.h"



typedef int(__cdecl *newint)(Vector*);
typedef int(__cdecl *newint2)(Vector*,int,char*);


int main()
{
	newint tmpCreate, tmpResize, tmpDestroy;
	newint2 tmpPush;
	int tmp;
	HINSTANCE testdll = LoadLibrary(TEXT("VectorDll.dll"));
	if (testdll != NULL) {
		tmpCreate = (newint)(GetProcAddress)(testdll, "Create");
		tmpResize = (newint)(GetProcAddress)(testdll, "Resize");
		tmpPush = (newint2)(GetProcAddress)(testdll, "Push");
		tmpDestroy = (newint)(GetProcAddress)(testdll, "Destroy");

		Vector v;
		tmp = tmpCreate(&v);
		char enter[255];
		for (int i = 0; i < 10; i++) {
			scanf("%s", enter);
			printf(":");
			tmp = tmpPush(&v, i, enter);
			printf("%s\n", v.word[i].mystring);
		}
		tmpDestroy(&v);
	
	}
	else printf("%d", GetLastError());
	FreeLibrary(testdll);
	system("Pause");
	return 0;
}
