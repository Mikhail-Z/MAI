#include <stdio.h>
#include <stdlib.h>
#include "Matrix.h"


typedef
struct pair
{
	int count;
	int col;
} pair;


// функция сравнения для сортировки
int cmp(const void* a, const void* b)
{
	// сравниваем по числу ненулевых
	const pair* x = (const pair*)a;
	const pair* y = (const pair*)b;
	if (x->count == y->count) {
		return y->col - x->col;
	}
	return y->count - x->count;
}


void task(Matrix m)
{
	pair* p = malloc(m.ncol * sizeof(pair));
	for (int j = 0; j < m.ncol; ++j) {
		p[j].count = 0;
		p[j].col = j;
		for (int i = 0; i < m.nrow; ++i) {
			real x = get_element(m, i, j);
			if (x) {
				++p[j].count;
			}
		}
	}
	// сортируем
	qsort(p, m.ncol, sizeof(pair), cmp);
	int J;	// искомый столбец
	// если таких столбцов несколько, нам нужен предпоследний
	if (m.ncol > 1 && p[0].count == p[1].count) {
		J = p[1].col;
	} else {
		J = p[0].col;
	}
	// произведение элементов столбца
	real prod = 1;
	for (int i = 0; i < m.nrow; ++i) {
		prod *= get_element(m, i, J);
	}
	printf("j = %d, product = %g\n", J, prod);
	free(p);
}


int main(int argc, char* argv[])
{
	// имя входного файла — это аргумент командной строки
	if (argc != 2) {
		printf("Usage: main input-file\n");
		return 0;
	}
	FILE* in = fopen(argv[1], "r");
	if (!in) {
		printf("Error: unable to open file\n");
		return 0;
	}
	int nrow, ncol;
	real r;
	// вначале во входном файле записаны размеры
	fscanf(in, "%d%d", &nrow, &ncol);
	Matrix m = new_matrix(nrow, ncol);
	// а затем матрица по строкам
	for (int i = 0; i < nrow; ++i) {
		for (int j = 0; j < ncol; ++j) {
			fscanf(in, "%lf", &r);
			if (r != 0.0) {
				set_element(m, i, j, r);
			}
		}
	}
	fclose(in);
	// печатаем во внутреннем представлении и в обычном виде
	print_inner(m);
	print(m);
	// делаем задание
	task(m);
	return 0;
}
