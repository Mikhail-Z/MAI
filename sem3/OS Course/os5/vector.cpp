#include "stdafx.h"
#include "Vector.h"


#ifdef __cplusplus
extern "C" {
#endif
	_declspec(dllexport) int _cdecl Create(Vector* v) {
		int res = 0;
		v->size = 0;
		if (v->word = (Item*)malloc(min_cap*sizeof(Item)))
			res = 1;
		v->capacity = min_cap;
		return res;
	}

	_declspec(dllexport) int _cdecl Resize(Vector* v) {
		int res = 0;
		if ((v->size + 1) > v->capacity) {
			v->capacity *= 2;
			if ((v->word = (Item*)realloc(v->word, sizeof(Item) * 256)))
				res = 1;
		}
		//strcpy_s(v->word[v->size].mystring,strlen(word), word);
		v->size++;
		return res;
	}

	_declspec(dllexport) int _cdecl Push(Vector *v, int position, char *str) {
		int res = 0;
		res = Resize(v);
		if (position < v->capacity) {
			strcpy(v->word[position].mystring, str);
		}
		return res;
	}

	_declspec(dllexport) void _cdecl Destroy(Vector* v) {
		free(v->word);
		v->size = 0;
		v->capacity = 0;
	}
#ifdef __cplusplus
}
#endif
