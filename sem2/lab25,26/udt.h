#ifndef UDT_H
#define UDT_H
#define MAXSIZE 20
#define key_type int
#define value_type int

typedef struct{
    key_type key;
    value_type value;
} data_type;

typedef struct
{
    data_type body[MAXSIZE];
    int size;
    int first;
} queue;

data_type pop_front(queue *);

void create(queue *);

int is_empty(queue *);

void push_back(queue *, const data_type);

void print(const queue *);

int size(const queue *);

void insert(queue *, const data_type);

//void erase(queue *, const key_type);

void insert(queue *, data_type); //добавление элемента в начало


#endif // UDT_H
