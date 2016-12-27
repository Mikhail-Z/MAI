// os67server.cpp : Defines the entry point for the console application.
//
#include <string.h>
#include <stdio.h>
#include "zmq.h"
#include <windows.h>
#include "stdafx.h"
#include <stdbool.h>
#include <stdlib.h>
#include <iostream>

#define MIN_CAP 2

struct Data
{
	unsigned long int allSum;
	int clientId;
};

struct Vector
{
	Data *data;
	int size;
	int capacity;
};

struct MessageData
{
	int clientId;
	int transactionId;
	int sum;
} MessageData;

struct MessageData2
{
    int FromClientId;
    int ToClientId;
	int transactionId;
	int sum;
	int action;
};

void Create(Vector *v) {
	v->data = (Data*)malloc(sizeof(Data)*MIN_CAP);
	v->size = 0;
	v->capacity = MIN_CAP;
}

void Resize(Vector *v) {
	if (v->size + 1 > v->capacity) {
		v->capacity *= 2;
		v->data = (Data*)realloc(v->data, v->capacity);
	}
	v->size++;
}

int Operation(Vector *v, MessageData2 inf)
{
	//printf("in operation\n");
	int i;
	for (i = 0; i < v->size; i++)
	{
		//std::cout << "id=" << inf.ToClientId << " v->id=" << v->data[i].clientId << std::endl;
		if (v->data[i].clientId == inf.ToClientId) {
			//printf("yes\n");
			if (v->data[i].allSum + inf.sum < 0)
				return -1;
			else if (inf.action == 1 || inf.action == 2) {
				v->data[i].allSum += inf.sum;
				return v->data[i].allSum;

			}
			else if (inf.action == 3) {
				v->data[i].allSum += inf.sum;
				return 1;
			}
		}
	}
		 if (i == v->size && inf.action != 3 && inf.action != 2) {
			Resize(v);
			v->data[v->size - 1].allSum = 0;
			v->data[v->size - 1].allSum += inf.sum;
			v->data[v->size - 1].clientId = inf.ToClientId;
			return v->data[v->size - 1].allSum;
			/*if (inf.sum < 0) {
				return 0;
			}*/
		}
		/*else  if (inf.action {
			v->data[v->size - 1].allSum += inf.sum;
			v->data[v->size - 1].clientId = inf.ToClientId;
			return v->data[v->size - 1].allSum;
		}*/
		 return 0;
}
	


int main(int argc, char const *argv[])
{
	int port;
	printf("Enter port you want to connect\n");
	scanf("%d", &port);
	/*if (port/1000 == 0 || port/10000 !=0) {
		printf("Wrong port. Enter port you want to connect again.\n");
		scanf("%d", &port);
	}*/
	Vector v;
	Create(&v);

	int totalNumOfTransactions = 0;
	char str[20];
	sprintf(str, "tcp://*:%d", port);
	void* context = zmq_ctx_new();
	void* serverSocket = zmq_socket(context, ZMQ_REP);
	zmq_bind(serverSocket, str);
	printf("Starting...\n");
	char c;
	for (;;)
	{
		fflush(stdin);
		printf("Do you want to stop server for 1 minute?\n");
		if ((c = getchar()) == 'y')
			Sleep(10000);

		zmq_msg_t message;
		zmq_msg_init(&message);
		zmq_msg_recv(&message, serverSocket, 0);
		MessageData2 *m = (MessageData2 *)zmq_msg_data(&message);
		if (m->action == 1) {
			std::cout << "Message from client: " << m->FromClientId << " messageId: " << m->transactionId << " sum: " << m->sum << std::endl;
			int res;
			char result[256];
			if (m->sum < 0) {
				//res = 0;
				sprintf(result, "You can't add a negative number! Maybe you wanted to choose the second action?");
			}
			else  {
				res = Operation(&v, *m);
				sprintf(result, "OK. Your total amount:%d\n", res);
			}
			zmq_msg_close(&message);
			
			zmq_msg_t reply;		
			zmq_msg_init_size(&reply, sizeof(result) + 1);
			memcpy(zmq_msg_data(&reply), result, sizeof(result) + 1);
			
			//memcpy(zmq_msg_data(&reply), "ok\0", 3);
			zmq_msg_send(&reply, serverSocket, 0);
			zmq_msg_close(&reply);
		}
		else if (m->action == 2) {
			std::cout << "Message from client: " << m->FromClientId << " messageId: " << m->transactionId << " sum: " << m->sum << std::endl;
			int res = Operation(&v, *m);
			zmq_msg_close(&message);

			zmq_msg_t reply;
			char result[256];
			if (res < 0) {
				sprintf(result, "You don't have so much money on your account!\n");
			}
			else
			sprintf(result, "OK. Your total amount:%d\n", res);
			zmq_msg_init_size(&reply, sizeof(result)+1);
			memcpy(zmq_msg_data(&reply), result, sizeof(result) + 1);
			//memcpy(zmq_msg_data(&reply), "ok\0", 3);
			zmq_msg_send(&reply, serverSocket, 0);
			zmq_msg_close(&reply);
		}
		else if (m->action == 3) {
			std::cout << "Message from client: " << m->FromClientId << " messageId: " << m->transactionId << " sum: " << m->sum << std::endl;
			int res;
			char result[256];
			if (m->sum <= 0) {
				res = 0;
				sprintf(result, "You can't put negative sum on another account!\n", res);
			}
			else {
				res = Operation(&v, *m);
				if (res==0)
					sprintf(result, "OK");
				else
					sprintf(result, "No such account!\n");
			}
			zmq_msg_close(&message);

			zmq_msg_t reply;
			zmq_msg_init_size(&reply, sizeof(result) + 1);
			memcpy(zmq_msg_data(&reply), result, sizeof(result) + 1);
			//memcpy(zmq_msg_data(&reply), "ok\0", 3);
			zmq_msg_send(&reply, serverSocket, 0);
			zmq_msg_close(&reply);
		}
		else if (m->action == 4) {
			std::cout << "Message from client: " << m->FromClientId <<std::endl;
			char result[256];
		    int res = m->FromClientId;
			sprintf(result, "Your account number is: %d\n", res);
			zmq_msg_t reply;
			zmq_msg_init_size(&reply, sizeof(result)+1);
			memcpy(zmq_msg_data(&reply), result, sizeof(result)+1);
			//memcpy(zmq_msg_data(&reply), "ok\0", 3);
			zmq_msg_send(&reply, serverSocket, 0);
			zmq_msg_close(&reply);
		}
		totalNumOfTransactions++;;
		
	}
	zmq_close(serverSocket);
	zmq_ctx_destroy(context);
	
	return 0;
}