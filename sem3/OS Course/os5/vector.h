#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>



#ifdef __cplusplus
extern "C" {
#endif

__declspec(dllexport)
const int min_cap = 4;

__declspec(dllexport)
typedef struct Item {
	char mystring[256];
};


__declspec(dllexport)
typedef struct Vector {
	Item *word;
	int size;
	int capacity;
};

 _declspec(dllexport) int _cdecl Create(Vector* v);
 _declspec(dllexport) int _cdecl Resize(Vector* v);
 _declspec(dllexport) void _cdecl Destroy(Vector* v);
 _declspec(dllexport) int _cdecl Push(Vector *v, int position, char *str);
#ifdef __cplusplus
}
#endif
