#pragma once

typedef	double	real;


typedef
struct Matrix
{
	// число строк
	int		nrow;
	// число столбцов
	int 	ncol;
	// мы храним матрицу по строкам
	// это векторы индексов
	int**	indexes;
	// а это векторы элементов
	real**	elements;
} Matrix;

// создание нулевой матрицы размером nrow x ncol
Matrix new_matrix(int nrow, int ncol);
// удаление матрицы
void delete_matrix(Matrix m);
// возвращает элемент с индексом (i, j)
real get_element(Matrix m, int i, int j);
// присваивает элементу значение: m[i][j] = x
void set_element(Matrix m, int i, int j, real x);
// печать внутренней структуры матрицы
void print_inner(Matrix m);
// печать матрицы
void print(Matrix m);
