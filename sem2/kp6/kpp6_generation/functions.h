#ifndef FUNCTIONS_H
#define FUNCTIONS_H
#include "point.h"

int append(FILE* filename, unit u);
int TxtToBin(char* text_name, FILE* f1);
void print(char* filename);
void zero(char* filename);

#endif // FUNCTIONS_H
