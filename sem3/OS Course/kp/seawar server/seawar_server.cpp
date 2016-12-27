#include "stdafx.h"
#include <stdio.h>
#include <conio.h>
#include <winsock2.h>
#include <windows.h>

#define MY_PORT 666
struct pair
{
	SOCKET first, second;	
	int game;
};

DWORD WINAPI LinkToClient(LPVOID client_socket);

int nclients = 0;
int game = 1;

int main(int argc, char* argv[])
{
	char buff[1024];
	printf("Sea War server.\n");

	if (WSAStartup(0x0202, (WSADATA *)&buff[0]))
	{
		printf("Error WSAStartup %d\n",
			WSAGetLastError());
		_getch();
		return -1;
	}
	SOCKET mysocket;

	if ((mysocket = socket(AF_INET, SOCK_STREAM, 0))<0)
	{
		printf("Error socket %d\n", WSAGetLastError());
		WSACleanup();
		_getch();
		return -1;
	}

	sockaddr_in local_addr;
	local_addr.sin_family = AF_INET;
	local_addr.sin_port = htons(MY_PORT);
	local_addr.sin_addr.s_addr = 0;

	if (bind(mysocket, (sockaddr *)&local_addr, sizeof(local_addr)))
	{
		printf("Error bind %d\n", WSAGetLastError());
		closesocket(mysocket);
		WSACleanup();
		_getch();
		return -1;
	}

	if (listen(mysocket, 0x100))
	{
		printf("Error listen %d\n", WSAGetLastError());
		closesocket(mysocket);
		WSACleanup();
		_getch();
		return -1;
	}

	printf("Wait for connections...\n");

	SOCKET client_socket;
	sockaddr_in client_addr;
	pair *p;

	int client_addr_size = sizeof(client_addr);

	while ((client_socket = accept(mysocket, (sockaddr *)&client_addr, &client_addr_size)))
	{
		if (nclients == 0)
		{
			p = new pair;
			p->first = client_socket;
			printf("Player %d connected to game %d.\n", nclients + 1, game);
		}
		else
		{
			printf("Player %d connected to game %d.\n", nclients + 1, game);
			p->second = client_socket;
			p->game = game;
			send(p->first, "OK1", 3, 0);
			send(p->second, "OK2", 3, 0);
			DWORD thID;

			CreateThread(NULL, NULL, LinkToClient, p, NULL, &thID);
			game++;
		}
		nclients++;
	}
	return 0;
}

DWORD WINAPI LinkToClient(LPVOID pair_of_clients)
{
	int phase = 1;	
	pair *p = (pair*)pair_of_clients;
	char buff[20 * 1024];
	int bytes_recv;
	do	
	{
		switch (phase)
		{
		case 0:
			bytes_recv = recv(p->first, buff, sizeof(buff), 0);
			
			if (bytes_recv != SOCKET_ERROR&&bytes_recv != 0)
				
				send(p->second, buff, bytes_recv, 0);
			
			if (memcmp(buff, "HIT", 3) == 0 || memcmp(buff, "KILL", 4) == 0)
				phase = 2;
			break;
		case 1:	
			bytes_recv = recv(p->first, buff, sizeof(buff), 0);
			if (bytes_recv != SOCKET_ERROR&&bytes_recv != 0)
				send(p->second, buff, bytes_recv, 0);
			break;
		case 2:	
			bytes_recv = recv(p->second, buff, sizeof(buff), 0);
			if (bytes_recv != SOCKET_ERROR&&bytes_recv != 0)
				send(p->first, buff, bytes_recv, 0);
			if (memcmp(buff, "HIT", 3) == 0 || memcmp(buff, "KILL", 4) == 0)
				phase = 0;
			break;
		case 3:
			bytes_recv = recv(p->second, buff, sizeof(buff), 0);
			if (bytes_recv != SOCKET_ERROR&&bytes_recv != 0)
				send(p->first, buff, bytes_recv, 0);
			break;
		}
		phase++;	
		phase &= 3;
	} while (bytes_recv != SOCKET_ERROR&&bytes_recv != 0);

	nclients -= 2;
	printf("Game %d closed.\n", p->game);
	// закрываем сокет
	closesocket(p->first);
	closesocket(p->second);
	delete p;
	return 0;
}