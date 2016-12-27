// os67client.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <time.h>
#include <string.h>
#include <stdio.h>
#include "zmq.h"
#include <iostream>
#include <Windows.h>
#define _CRT_SECURE_NO_WARNINGS
typedef struct MD
{
	int FromClientId;
    int ToClientId;
	int transactionId;
	int sum;
	int action;
} MessageData;

int main(int argc, char const *argv[])
{
	int port;
	printf("Enter port you want to connect\n");
	//while (1)
	std::cin>>port;
	/*if (port / 1000 == 0 || port / 10000 != 0) {
		printf("Wrong port. Enter port you want to connect again.\n");
		std::cin>>port;
	}*/

	char str[20];
	sprintf(str, "tcp://localhost:%d", port);

	void* context = zmq_ctx_new();
	srand(time(0));
	int clientId;
	printf("Enter number of your account\n");
	char tmp[256];
	while (1) {
		std::cin >> tmp;
		int len = strlen(tmp);
		if (len<=9 && tmp[0]!='-') {
			clientId = atoi(tmp);
			memset(tmp, '\0', sizeof(tmp));
			break;
		}
		else printf("Wrong account number! please, enter again!\n");
		memset(tmp, '\0', sizeof(tmp));
	}
	//std::cin>>clientId;
	printf("Client %d Starting...\n", clientId);
	char cmd[256];
	void* senderSocket = zmq_socket(context, ZMQ_REQ);
	zmq_connect(senderSocket, str);
	int count = 0;
	int n;
	int sum;
	for (;;)
	{		
		printf("Chooce your action: 1 - put money in bank on my count; 2 - take off money from my count; 3 - put money in bank on another count; 4 - want to know the number of my count; 5 - quit\n");
		fflush(stdin);
		std::cin >> cmd;
		if (strcmp(cmd,"1")==0) {
			MessageData md;
			md.FromClientId = clientId;
			md.ToClientId = clientId;
			md.transactionId = count;	
			printf("Enter necessary sum\n");
			while (1) {
				std::cin >> tmp;
				if (strlen(tmp)<=9) {
					sum = atoi(tmp);
					memset(tmp, '\0', sizeof(tmp));
					break;
				}
				else
					std::cout << "Too big sum of money! Max sum is 999 999 999 per operation!\n" << std::endl;
				memset(tmp, '\0', sizeof(tmp));
			}
			md.sum = sum;
			md.action = 1;
			
			zmq_msg_t zmqMessage;
			zmq_msg_init_size(&zmqMessage, sizeof(MessageData));
			memcpy(zmq_msg_data(&zmqMessage), &md, sizeof(MessageData));

			printf("Sending: - %d\n", count);
			int send = zmq_msg_send(&zmqMessage, senderSocket, 0);
			zmq_msg_close(&zmqMessage);
			
			/*zmq_msg_t reply;
			zmq_msg_init(&reply);
			zmq_msg_recv(&reply, senderSocket, 0);
			size_t repSize = zmq_msg_size(&reply);
			printf("Received: - %d %s\n", repSize, zmq_msg_data(&reply));
			zmq_msg_close(&reply);*/

			//Sleep(1000);
			count++;
		}
			
		else if (strcmp(cmd, "2") == 0) {
			MessageData md;
			md.FromClientId = clientId;
			md.ToClientId = clientId;
			md.transactionId = count;
			printf("Enter necessary sum\n");

			while (1) {
				std::cin >> tmp;
				if (strlen(tmp)<=9) {
					sum = atoi(tmp);
					memset(tmp, '\0', sizeof(tmp));
					break;
				}
				else
					std::cout << "Too big sum of money! Max sum is 999 999 999 per operation!\n" << std::endl;
				memset(tmp, '\0', sizeof(tmp));
			}
			md.sum = -abs(sum);
			md.action = 2;
			zmq_msg_t zmqMessage;
			zmq_msg_init_size(&zmqMessage, sizeof(MessageData));
			memcpy(zmq_msg_data(&zmqMessage), &md, sizeof(MessageData));

			printf("Sending: - %d\n", count);
			int send = zmq_msg_send(&zmqMessage, senderSocket, 0);
			zmq_msg_close(&zmqMessage);

			/*zmq_msg_t reply;
			zmq_msg_init(&reply);
			zmq_msg_recv(&reply, senderSocket, 0);
			size_t repSize = zmq_msg_size(&reply);
			printf("Received: - %d %s\n", repSize, zmq_msg_data(&reply));
			zmq_msg_close(&reply);*/

			//Sleep(1000);
			count++;
		}

		else if (strcmp(cmd, "3") == 0) {
			MessageData md;
			printf("Enter bank account where you want to send?\n");
			while (1) {
				std::cin >> tmp;
				int len = strlen(tmp);
				if (len <= 9 && tmp[0] != '-') {
					md.ToClientId = atoi(tmp);
					memset(tmp, '\0', sizeof(tmp));
					break;
				}
				else printf("Wrong account number! please, enter again!\n");
				memset(tmp, '\0', sizeof(tmp));
			}
			
			md.FromClientId = clientId;
			md.transactionId = count;
			printf("Enter necessary sum\n");
			while (1) {
				std::cin >> tmp;
				if (strlen(tmp) <= 9) {
					sum = atoi(tmp);
					memset(tmp, '\0', sizeof(tmp));
					break;
				}
				else
					std::cout << "Too big sum of money! Max sum is 999 999 999 per operation!\n" << std::endl;
				memset(tmp, '\0', sizeof(tmp));
			}
			//md.sum = abs(sum);
			md.action = 3;
			zmq_msg_t zmqMessage;
			zmq_msg_init_size(&zmqMessage, sizeof(MessageData));
			memcpy(zmq_msg_data(&zmqMessage), &md, sizeof(MessageData));

			printf("Sending: - %d\n", count);
			int send = zmq_msg_send(&zmqMessage, senderSocket, 0);
			zmq_msg_close(&zmqMessage);

			/*zmq_msg_t reply;
			zmq_msg_init(&reply);
			zmq_msg_recv(&reply, senderSocket, 0);
			size_t repSize = zmq_msg_size(&reply);
			printf("Received: - %d %s\n", repSize, zmq_msg_data(&reply));
			zmq_msg_close(&reply);*/

			//Sleep(1000);
			count++;
		}

		else if (strcmp(cmd, "4") == 0){
			MessageData md;
			md.action = 4;
			md.FromClientId = clientId;
			md.sum = NULL;
			md.transactionId = count;
			zmq_msg_t zmqMessage;
			zmq_msg_init_size(&zmqMessage, sizeof(MessageData));
			memcpy(zmq_msg_data(&zmqMessage), &md, sizeof(MessageData));

			printf("Sending: - %d\n", count);
			int send = zmq_msg_send(&zmqMessage, senderSocket, 0);
			zmq_msg_close(&zmqMessage);

			/*zmq_msg_t reply;
			zmq_msg_init(&reply);
			zmq_msg_recv(&reply, senderSocket, 0);
			size_t repSize = zmq_msg_size(&reply);
			printf("Received: - %d %s\n", repSize, zmq_msg_data(&reply));
			zmq_msg_close(&reply);*/

			//Sleep(1000);
			count++;
		}

		else if (strcmp(cmd, "5") == 0) {
			zmq_close(senderSocket);
			zmq_ctx_destroy(context);
			return 0;
		}
		else {
			printf("Wrong action! Please, enter again!\n");
			continue;
		}
		zmq_msg_t reply;
		zmq_msg_init(&reply);
		zmq_msg_recv(&reply, senderSocket, 0);
			
		size_t repSize = zmq_msg_size(&reply);
		printf("Received: - %s\n", zmq_msg_data(&reply));
		zmq_msg_close(&reply);
		
		/*MessageData md;
		md.clientId = clientId;
		md.messageNumber = count;
		zmq_msg_t zmqMessage;
		zmq_msg_init_size(&zmqMessage, sizeof(MessageData));
		memcpy(zmq_msg_data(&zmqMessage), &md, sizeof(MessageData));

		printf("Sending: - %d\n", count);
		int send = zmq_msg_send(&zmqMessage, senderSocket, 0);
		zmq_msg_close(&zmqMessage);

		zmq_msg_t reply;
		zmq_msg_init(&reply);
		zmq_msg_recv(&reply, senderSocket, 0);
		size_t repSize = zmq_msg_size(&reply);
		printf("Received: - %d %s\n", repSize, zmq_msg_data(&reply));
		zmq_msg_close(&reply);

		Sleep(1000);
		count++;*/
	}
	// We never get here though.
	zmq_close(senderSocket);
	zmq_ctx_destroy(context);

	return 0;
}