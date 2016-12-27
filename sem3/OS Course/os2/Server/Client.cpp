// Client.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <conio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define _CRT_SECURE_NO_WARNINGS

typedef struct _tnode tnode;
struct _tnode {
	int data;
	tnode *parent;
	tnode *prev;
	tnode *next;
	tnode *child;
};

typedef struct _vector vector;
struct _vector {
	int *data;
	int size;
};

tnode *add(tnode **node, const int value) {
	tnode *pnext = NULL;
	tnode *p = (tnode *)malloc(sizeof(tnode));
	p->data = value;
	p->parent = NULL;
	p->prev = NULL;
	p->next = NULL;
	p->child = NULL;
	if (*node == NULL)
		*node = p;
	else if ((*node)->child == NULL) {
		p->parent = *node;
		(*node)->child = p;
	}
	else {
		pnext = (*node)->child;
		while (pnext->next != NULL)
			pnext = pnext->next;
		p->parent = *node;
		p->prev = pnext;
		pnext->next = p;
	}
	return p;
}

tnode *find(tnode **node, const int value) {
	printf("value = %d\n", value);
	tnode *p = NULL;
	if ((*node) == NULL)
		return p;
	if ((*node)->data == value)
		p = *node;
	else if ((*node)->next != NULL)
		p = find(&(*node)->next, value);
	if (p == NULL && (*node)->child != NULL)
		p = find(&(*node)->child, value);
	return p;
}

void destroy(tnode **node) {
	if (*node == NULL)
		return;
	if ((*node)->next != NULL)
		destroy(&(*node)->next);
	if ((*node)->child != NULL)
		destroy(&(*node)->child);
	free(*node);
	*node = NULL;
}

void print_tree(tnode **node, const int level) {
	printf("%*s%d\n", level * 2, "", (*node)->data);
	if ((*node)->child != NULL)
		print_tree(&(*node)->child, level + 1);
	if ((*node)->next != NULL)
		print_tree(&(*node)->next, level);
}

bool remove_node(tnode **node, const int value) {
	if (!&node) return 0;
	tnode *p = find(node, value);
	if (p == NULL)
		return 0;
	if (p->parent == NULL) {
		destroy(node);
		return 1;
	}
	if (p->prev == NULL)
		p->parent->child = p->next;
	else
		p->prev->next = p->next;
	if (p->next != NULL)
		p->next->prev = p->prev;
	if (p->child != NULL)
		destroy(&p->child);
	free(p);
	p = NULL;
	return 1;
}

int num_nodes(tnode *t) {
	if (t == NULL)
		return 0;
	return 1 + num_nodes(t->child) + num_nodes(t->next);
}

int height(tnode *t) {
	if (t == NULL)
		return 0;
	int a = 1 + height(t->child), b = height(t->next);
	return (a > b ? a : b);
}

int num_leaves(tnode *t) {
	if (t == NULL)
		return 0;
	if (t->child == NULL)
		return 1 + num_leaves(t->next);
	return num_leaves(t->child) + num_leaves(t->next);
}

tnode *node_by_path(tnode **node, char *path) {
	int i = 0;
	tnode *p = *node;
	while (path[i] != '\0') {
		if (path[i] == 's')
			if (p->child != NULL)
				p = p->child;
			else
				return NULL;
		else if (path[i] == 'b')
			if (p->next != NULL)
				p = p->next;
			else
				return NULL;
		else
			return NULL;
		i++;
	}
	return p;
}

int main(int argc, char *argv[])
{

	tnode *tree = NULL, *p = NULL;
	HANDLE inH = GetStdHandle(STD_INPUT_HANDLE);
	HANDLE outH = GetStdHandle(STD_OUTPUT_HANDLE);
	char command[256];
	char arg1[3], arg2[244], arg3[11];
	int i;
	char* pch;
	//int l;
	int val;
	int result;
	DWORD readBytes, writeBytes;
	while (ReadFile(inH, command, sizeof(command), &readBytes, NULL))
	{
		memset(arg1, '\0', 3);
		memset(arg2, '\0', 244);
		memset(arg3, '\0', 11);
		i = 0;
		pch = strtok(command, " ");
		while (pch != '\0')
		{
			switch (i)
			{
			case 0:
				strcpy(arg1, pch);
				break;
			case 1:
				strcpy(arg2, pch);
				break;
			case 2:
				strcpy(arg3, pch);
				break;
			}
			pch = strtok(NULL, " ");
			i++;
		}
		switch (arg1[0]) {

		case '+':
			if (arg1[1] == 'r') {
				if (tree != NULL) {
					result = -1;
					if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
						return -2;
					break;
				}
				else {
					val = atoi(arg2);
					if (add(&tree, val) != NULL)
						if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
							return -2;

				}
			}
		    else if (arg1[1] == 's') {
				val = atoi(arg2);			
				p = node_by_path(&tree, &arg1[1]);
				if (p == NULL) {
					result = -3;
					if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
						return -2;
					break;
				}
				if (add(&p, val)) {
					if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
						return -2;
				}
		    }
			else {
				val = atoi(arg2);
				if (add(&tree, val)) {
					if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
						return -2;
				}
			}
			break;

		case '-':
			if (arg2[0] >= '0' && arg2[0] <= '9') {
				val = atoi(arg2);
				if (remove_node(&tree, val)) {
					result = 1;
					if (!WriteFile(outH, &result, sizeof(int), &readBytes, NULL))
						return -2;
				}
				else {
					result = 0;
					printf("%d\n", result);
					if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
						return -2;
				}
			}
			else {
				result = -10;
				if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
					return -2;
			}
			break;

		case 'n':
			val = num_nodes(tree);
			if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
				return -2;
			break;

		case 's':
			
			for (i = 0; i < sizeof(arg2); i++)
			{
				if (arg2[i] == '\n')
				{
					arg2[i] = '\0';
					break;
				}
			}
			p = node_by_path(&tree, arg2);
			if (p)
				result = p->data;
			else result = 0;
			if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
				return -2;
			break;

		case 't':
			if (arg2[0] >= '0' && arg2[0] <= '9') {
				val = atoi(arg2);
				p = find(&tree, val);

				if (p) result = 1;
				else result = 0;
				p = NULL;
			}
			if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
				return -2;
			break;

		case 'l':
			val = num_leaves(tree);
			if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
				return -2;
			break;
		case 'v':
			val = height(tree);
			if (!WriteFile(outH, &val, sizeof(int), &writeBytes, NULL))
				return -2;
			break;

		default:
			result = -11;
			if (!WriteFile(outH, &result, sizeof(int), &writeBytes, NULL))
				return -2;
			break;
		}
	}

	return 0;

}
