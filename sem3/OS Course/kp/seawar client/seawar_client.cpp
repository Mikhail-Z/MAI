#include "stdafx.h"
#include <stdio.h>
#include <iostream>
#include <conio.h>
#include <string.h>
#include <winsock2.h>
#include <windows.h>

#define PORT 666
#define SERVERADDR "127.0.0.1"

#define sz 10	

bool first = false;	

char getval(char f[sz][sz], int r, int c)
{
	
	if (r<0 || r >= sz)
		return ' ';
	if (c<0 || c >= sz)
		return ' ';
	return f[r][c];
}

struct pair {
	int x;
	int y;
};

struct Vector {
	pair *pair;
	int size;
};

void Create(Vector *v, int size) {
	v->size = size;
	v->pair = (pair*)malloc(sizeof(pair)*size);
}

void Delete(Vector *v) {
	free(v->pair);
}

void show(char f[sz][sz])
{
	printf("  ");
	int i;
	for (i = 0; i < sz; i++)
		printf("%d", (i + 1) % 10);
	printf("\n");
	for (i = 0; i < sz; i++) {
		printf("%c ", 'A' + i);
		for (int j = 0; j < sz; j++)
			printf("%c", f[i][j]);
		printf("\n");
	}
}

void proverka(Vector *tmp, char field[10][10], int size) {
	int i = 0;
	char c;
	int flag = -1;
	while (i<size) {
		std::cin >> c;
		tmp->pair[i].y = c - 'A';
		scanf("%d",&tmp->pair[i].x);

		tmp->pair[i].x--;

		if (tmp->pair[i].x > 9 || tmp->pair[i].x < 0 || tmp->pair[i].y < 0 || tmp->pair[i].y > 9) {
			printf("wrong coordinate 1! Enter all coordinates of the ship again!\n");
			i = 0;
			continue;
		}
		else if (field[tmp->pair[i].y][tmp->pair[i].x] == 'Û') {
			printf("wrong coordinate 2! Enter all coordinates of the ship again!\n");
			i = 0;
			continue;
		}
		else {
			if (tmp->pair[i].x > 0) {
				if (field[tmp->pair[i].y][tmp->pair[i].x - 1] == 'Û') {
					printf("wrong coordinate 3 Enter all coordinates of the ship again!\n");
					i = 0;
					continue;
				}
			}
			if (tmp->pair[i].x<9) {
				if (field[tmp->pair[i].y][tmp->pair[i].x + 1] == 'Û') {
					printf("wrong coordinate 4! Enter all coordinates of the ship again!\n");
					i = 0;
					continue;
				}
			}
			if (tmp->pair[i].y > 0) {
				if (field[tmp->pair[i].y - 1][tmp->pair[i].x] == 'Û') {
					printf("wrong coordinate 5! Enter all coordinates of the ship again!\n");
					i = 0;
					continue;
				}
			}
			if (tmp->pair[i].y<9) {
				if (field[tmp->pair[i].y + 1][tmp->pair[i].x] == 'Û') {
					printf("wrong coordinate 6! Enter all coordinates of the ship again!\n");
					i = 0;
					continue;
				}
			}
			if (i == 1) {

				if (tmp->pair[i].x == tmp->pair[i - 1].x + 1 && tmp->pair[i].y == tmp->pair[i - 1].y)
					flag = 0;
				else if (tmp->pair[i].y == tmp->pair[i - 1].y + 1 && tmp->pair[i].x == tmp->pair[i - 1].x)
					flag = 1;
				else {
					printf("wrong coordinate 7! Enter all coordinates of the ship again!\n");
					i = 0;
					continue;
				}
			}
			else if (i > 1) {
				if (flag == 0) {
					if (tmp->pair[i].x != tmp->pair[i - 1].x + 1 || tmp->pair[i].y != tmp->pair[i-1].y) {
						printf("wrong coordinate 8! Enter all coordinates of the ship again!\n");
						i = 0;
						continue;
					}
				}
				else if (flag == 1) {
					if (tmp->pair[i].y != tmp->pair[i - 1].y + 1 || tmp->pair[i].x != tmp->pair[i-1].x) {
						printf("wrong coordinate 9! Enter all coordinates of the ship again!\n");
						i = 0;
						continue;
					}
				}
			}

		}
		i++;
	}
}

void fieldCreation(char field[sz][sz]) {
	int i, j;

	show(field);
	char x;
	int y;
	int number;
	printf("Enter data about ships (Example: A1)\n");
	printf("firstly, enter data about one biggest (4) ship\n");
	number = 1;
	Vector tmp;
	int ship_size = 4;
	char c;
	int flag = -1;
	Create(&tmp, 4);
	for (i = 0; i < number; i++) {
		proverka(&tmp, field, ship_size);
		for (j = 0; j < ship_size; j++) {
			field[tmp.pair[j].y][tmp.pair[j].x] = 'Û';
		}
		show(field);
	}
	Delete(&tmp);
	fflush(stdin);
	printf("secondly, enter data about two smaller (3) ships\n");
	Create(&tmp, 3);
	ship_size = 3;
	number = 2;
	for (i = 0; i < number; i++) {
		proverka(&tmp, field, ship_size);
		for (j = 0; j < ship_size; j++) {
			field[tmp.pair[j].y][tmp.pair[j].x] = 'Û';
		}
		show(field);
	}
	Delete(&tmp);

	printf("thirdly, enter data about three smaller (2) ships\n");
	Create(&tmp, 2);
	ship_size = 2;
	number = 3;
	for (i = 0; i < number; i++) {
		proverka(&tmp, field, ship_size);
		for (j = 0; j < ship_size; j++) {
			field[tmp.pair[j].y][tmp.pair[j].x] = 'Û';
		}
		show(field);
	}
	Delete(&tmp);

	printf("fourthly, enter data about four smallest (1) ships\n");
	Create(&tmp, 1);
	ship_size = 1;
	number = 4;
	for (i = 0; i < number; i++) {
		proverka(&tmp, field, ship_size);
		for (j = 0; j < ship_size; j++) {
			field[tmp.pair[j].y][tmp.pair[j].x] = 'Û';
		}
		show(field);
	}
	Delete(&tmp);
	std::cout<<"OK, you have entered all ships!"<<std::endl;
	fflush(stdin);
}



bool checkmove(char *move, int *r, int *c)
{
	move[0] = toupper(move[0]);
	if (move[0]<'A' || move[0]>'J')
		return false;
	*r = move[0] - 'A';	
	*c = atoi(&move[1]) - 1;
	if (*c<0 || *c>9)	
		return false;	
	return true;
}

int main(int argc, char* argv[])
{
	char my[sz][sz] = {
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
		{ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' },
	};
	char buff[1024];
	printf("Sea War client.\n");
	if (WSAStartup(0x202, (WSADATA *)&buff[0]))
	{
		printf("WSAStart error %d\n", WSAGetLastError());
		_getch();	
		return -1;
	}
	SOCKET my_sock;
	my_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (my_sock < 0)
	{
		printf("Socket() error %d\n", WSAGetLastError());
		_getch();
		return -1;
	}

	sockaddr_in dest_addr;
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(PORT);
	HOSTENT *hst;

	if (inet_addr(SERVERADDR) != INADDR_NONE) {
		dest_addr.sin_addr.s_addr = inet_addr(SERVERADDR);
	}
	else {

			printf("Invalid address %s\n", SERVERADDR);
			closesocket(my_sock);
			WSACleanup();
			return -1;

	}

	if (connect(my_sock, (sockaddr *)&dest_addr, sizeof(dest_addr)))
	{
		printf("Connect error %d\n", WSAGetLastError());
		_getch();
		return -1;
	}
	char res[256] = { 0 };
	printf("Wait for another player...\n");
	int nsize = recv(my_sock, buff, sizeof(buff) - 1, 0);
	if (nsize == SOCKET_ERROR)
	{
		printf("Recv error %d\n", WSAGetLastError());
		closesocket(my_sock);
		WSACleanup();
		_getch();
		return -1;
	}
	if (buff[0] != 'O' || buff[1] != 'K')
	{
		printf("Recv error %d\n", WSAGetLastError());
		closesocket(my_sock);
		WSACleanup();
		_getch();
		return -1;
	}
	first = (buff[2] == '1');
	int r, c, t, dl, pop;
	printf("You are %s player.\n", first ? "first" : "second");
	fieldCreation(my);

	while (1)
	{
		if (first)
		{
			do
			{
				while (1)
				{
					printf("Your move (or quit): "); fflush(stdin); while(fgets(&buff[0], sizeof(buff) - 1, stdin)==0);
				
					if (!strcmp(&buff[0], "quit\n"))
					{
					
						closesocket(my_sock);
						WSACleanup();
						return 0;
					}
					if (checkmove(buff, &r, &c))
						break;
					else printf("wrong move! enter again.\n");
				}
				if (send(my_sock, buff, strlen(buff), 0) == 0)
				{
					printf("Send error %d\n", WSAGetLastError());
					closesocket(my_sock);
					WSACleanup();
					_getch();
					return -1;
				}
				nsize = recv(my_sock, buff, sizeof(buff) - 1, 0);
				if (nsize == SOCKET_ERROR || nsize == 0)
				{
					printf("Recv error %d\n", WSAGetLastError());
					closesocket(my_sock);
					WSACleanup();
					_getch();
					return -1;
				}
				buff[nsize] = 0;
				printf("%s\n", buff);
			} while (memcmp(buff, "HIT", 3) == 0 || memcmp(buff, "KILL", 4) == 0);
			if (strcmp(buff, "YOU WIN") == 0)
			{
				closesocket(my_sock);
				WSACleanup();
				_getch();
				return 0;

			}
		}
		else std::cout << "Waiting for your opponent move" << std::endl;
		do
		{
			nsize = recv(my_sock, buff, sizeof(buff) - 1, 0);
			if (nsize == SOCKET_ERROR || nsize == 0)
			{
				printf("Recv error %d\n", WSAGetLastError());
				closesocket(my_sock);
				WSACleanup();
				_getch();
				return -1;
			}
			buff[nsize] = 0;

			printf("%s\n", buff);

			checkmove(buff, &r, &c);

			if (getval(my, r, c) == 'Û')
			{
				my[r][c] = '*';	

				if (getval(my, r + 1, c) == ' '&&getval(my, r - 1, c) == ' '&&getval(my, r, c + 1) == ' '&&getval(my, r, c - 1) == ' ')
				{
					int ost = 0;	
					for (int i = 0; i<sz; i++)
						for (int j = 0; j<sz; j++)
							ost += (my[i][j] == 'Û');
					if (ost)
						strcpy(res, "KILL");
					else	
						strcpy(res, "YOU WIN");
				}

				else if (getval(my, r + 1, c) != ' ' || getval(my, r - 1, c) != ' ')
				{
					for (t = r; getval(my, t, c) != ' '; t--);
					pop = 0;
					for (dl = 0, t++; getval(my, t, c) != ' '; t++, dl++)
						pop += (getval(my, t, c) == '*');
				}
				else
				{
					for (t = c; getval(my, r, t) != ' '; t--);
					pop = 0;
					for (dl = 0, t++; getval(my, r, t) != ' '; t++, dl++)
						pop += getval(my, r, t) == '*';
				}
				if (pop == dl)
				{
					int ost = 0;
					for (int i = 0; i<sz; i++)
						for (int j = 0; j<sz; j++)
							ost += my[i][j] == 'Û';
					if (ost)
						strcpy(res, "KILL");
					else
						
						strcpy(res, "YOU WIN");
				}
				else
					strcpy(res, "HIT");
			}
			else
				strcpy(res, "MISS");
			show(my);
			if (send(my_sock, res, strlen(res), 0) == 0)
			{
				printf("Send error %d\n", WSAGetLastError());
				closesocket(my_sock);
				WSACleanup();
				_getch();
				return -1;
			}
			
			first = true;
			
		} while (memcmp(res, "HIT", 3) == 0 || memcmp(res, "KILL", 4) == 0);
		
		if (strcmp(res, "YOU WIN") == 0)
		{
			printf("Game Over\n");
			closesocket(my_sock);
			WSACleanup();
			_getch();
			return 0;
		}
	}
	printf("Recv error %d\n", WSAGetLastError());
	closesocket(my_sock);
	WSACleanup();
	_getch();
	return -1;
}