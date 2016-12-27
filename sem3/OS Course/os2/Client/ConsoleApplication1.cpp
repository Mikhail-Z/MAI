// ConsoleApplication1.cpp : Defines the entry point for the console application.
//


#include "stdafx.h"
#include <Windows.h>
#include <stdbool.h>
#include <stdio.h>
#include "string.h"

int main(int argc, char **argv)
{
	SECURITY_ATTRIBUTES sa;
	sa.nLength = sizeof(SECURITY_ATTRIBUTES);
	sa.lpSecurityDescriptor = NULL;
	sa.bInheritHandle = TRUE;

	PROCESS_INFORMATION ProcessInfo;
	ZeroMemory(&ProcessInfo, sizeof(PROCESS_INFORMATION));
	STARTUPINFO StartupInfo;
	TCHAR lpszClientPath[] = L"client.exe";
	ZeroMemory(&StartupInfo, sizeof(StartupInfo));
	StartupInfo.cb = sizeof(STARTUPINFO);
	HANDLE pipe1Read, pipe1Write, pipe2Read, pipe2Write;
	CreatePipe(&pipe1Read, &pipe1Write, &sa, 0);
	CreatePipe(&pipe2Read, &pipe2Write, &sa, 0);
	StartupInfo.dwFlags = STARTF_USESTDHANDLES;
	StartupInfo.hStdInput = pipe1Read;
	StartupInfo.hStdOutput = pipe2Write;

	bool process = CreateProcess(NULL,
		lpszClientPath,
		NULL, NULL, true,
		CREATE_NEW_CONSOLE,
		NULL, NULL,
		&StartupInfo,
		&ProcessInfo);
	CloseHandle(pipe1Read);
	CloseHandle(pipe2Write);



	printf("Enter commands (h - help). Note, that the first command should be +r val.\n");
	//пишем в анонимный канал
	char command[256];
	memset(command, '\0', 256);
	int result;

		while(fgets(command, sizeof(command), stdin)) {
	
		if (command[0] == 'h') {
			printf("------------------------------\n");
			printf("List of commands:\n");
			printf("+r VAL - create node VAL\n");
			printf("+ VAL - add VAL to root\n");
			printf("+ PATH VAL - add node VAL on PATH (s - son, b - sibling)\n");
			printf("- VAL - remove first node VAL\n");
			printf("p - print tree\n");
			printf("n - number of nodes\n");
			printf("l - number of leaves\n");
			printf("v - height\n");
			printf("s PATH - search by path\n");
			printf("t VAL - search by value\n");
			printf("q - quit\n");
			printf("------------------------------\n");
		}
		else {
			DWORD dwBytesWrite, dwBytesRead;
			if (!WriteFile(pipe1Write, command, sizeof(command), &dwBytesWrite, NULL))
			{
				printf("Write to file failed. Error %d\n", GetLastError());
			}
			if (ReadFile(pipe2Read, &result, sizeof(result), &dwBytesRead, NULL))
				printf("%d\n", result);
			else printf("I haven't read\n");

		}
		memset(command, '\0', 256);
	}

	CloseHandle(pipe2Read);
	CloseHandle(pipe1Write);
	CloseHandle(ProcessInfo.hThread);
	CloseHandle(ProcessInfo.hProcess);
	system("pause");

	return 0;
}



