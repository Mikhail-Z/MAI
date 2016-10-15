#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Matrix.h"


// создание нулевой матрицы размером nrow x ncol
Matrix new_matrix(int nrow, int ncol)
{
	Matrix m;
	m.nrow = nrow;
	m.ncol = ncol;
	m.indexes = malloc(nrow * sizeof(int*));
	m.elements = malloc(nrow * sizeof(real*));
	for (int i = 0; i < nrow; ++i) {
		m.indexes[i] = malloc(sizeof(int));
		// специальное значение, означающее конец вектора
		m.indexes[i][0] = -1;
		m.elements[i] = NULL;
	}
	return m;
}


// удаление матрицы
void delete_matrix(Matrix m)
{
	for (int i = 0; i < m.nrow; ++i) {
		free(m.indexes[i]);
		free(m.elements[i]);
	}
	free(m.indexes);
	free(m.elements);
}


// возвращает элемент с индексом (i, j)
real get_element(Matrix m, int i, int j)
{
	if (i < 0 || i >= m.nrow || j < 0 || j >= m.ncol) {

		printf("index (%d, %d) is out of range\n", i, j);
		// или поставить assert
		return 0;
	}
	// i-я строка
	int* row = m.indexes[i];
	// индекс элемента, который обозначен лямбдой
	int idx = i * m.ncol + j;

	int k = 0;
	// ищем нужный индекс
	for (; row[k] != -1; ++k) {
		if (row[k] == idx) {
			break;
		}
	}
	if (row[k] == -1) {
		// элемента в таблице нет, значит он равен нулю
		return 0;
	} else {
		return m.elements[i][k];
	}
}


// присваивает элементу значение: m[i][j] = x
void set_element(Matrix m, int i, int j, real x)
{
	if (i < 0 || i >= m.nrow || j < 0 || j >= m.ncol) {
		// если индекс вне границ, ничего не делаем
		return;
	}
	// такой же как и в get_element поиск элемента
	int* row = m.indexes[i];
	int idx = i * m.ncol + j;
	int k = 0;
	for (; row[k] != -1 && row[k] <= idx; ++k);
	if (row[k] == -1 || row[k] > idx) {

		int count = k;
		for (; row[count] != -1; ++count);
		int* p = malloc((count + 2) * sizeof(int));
		if (!p) {
			// памяти нет, ничего не делаем
			printf("Error: unable allocate memory\n");
			return;
		}
		// копируем элементы до индекса idx
		memcpy(p, row, k * sizeof(int));
		p[k] = idx;
		memcpy(p + k + 1, row + k, (count - k + 1) * sizeof(int));
		// уничтожаем старую память
		free(row);
		m.indexes[i] = p;
		// проделываем такую же операцию с элементами
		real* ptr = malloc((count + 1) * sizeof(real));
		real* e = m.elements[i];
		memcpy(ptr, e, k * sizeof(real));
		ptr[k] = x;
		memcpy(ptr + k + 1, e + k, (count - k) * sizeof(real));
		free(e);
		m.elements[i] = ptr;
	} else {
		// если элемент уже есть, просто меняем значение на новое
		m.elements[i][k] = x;
	}
}


void print_inner(Matrix m)
{
	for (int i = 0; i < m.nrow; ++i) {
		int* row = m.indexes[i];
		real* e = m.elements[i];
		printf("{[");
		for (int j = 0; row[j] != -1; ++j) {
			printf(" %d", row[j]);
		}
		printf(" -1]\n");
		printf(" [");
		for (int j = 0; row[j] != -1; ++j) {
			printf(" %g", e[j]);
		}
		printf("]}\n");
	}
}


void print(Matrix m)
{
	for (int i = 0; i < m.nrow; ++i) {
		int* row = m.indexes[i];
		real* e = m.elements[i];
		printf("|");
		int idx = i * m.ncol;
		for (int j = 0, k = 0; j < m.ncol; ++j, ++idx) {
			if (row[k] == idx) {
				printf("%5g", e[k]);
				++k;
			} else {
				printf("%5g", 0.0);
			}
		}
		printf("|\n");
	}
}
