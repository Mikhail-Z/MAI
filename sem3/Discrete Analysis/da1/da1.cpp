#include <cstdlib>
#include <iostream>
#include <string>
#include <ctime>
#define MIN_CAP 8

using namespace std;

typedef struct{
    size_t key;
    string* value;
} TElem;

typedef struct{
    TElem* body;
    size_t size;
    size_t cap;
} TVector;

typedef struct{
    size_t* body;
    size_t size;
} TIntVector;

TVector* Create(){
    TVector *v = (TVector*)malloc(sizeof(TVector));
    v->size = 0;
    v->body = (TElem*)malloc(sizeof(TElem)*MIN_CAP);
    for (size_t i = 0; i < MIN_CAP; i++){
        v->body[i].value = new string;
    }
    v->cap = MIN_CAP;
    return v;
}

TIntVector* CreateIntv(size_t size, size_t min){
    TIntVector *v = (TIntVector*)malloc(sizeof(TIntVector));
    v->size = size;
    v->body = (size_t*)malloc(sizeof (size_t)*size);
    if (min == 0){
        min = 1;
    }
    for (size_t i = min - 1; i < v->size; ++i){
        v->body[i] = 0;
    }
    return v;
}

void SetSize(TVector* v, size_t size){
    v->size = size;
    v->body = new TElem[v->size];
}

size_t CalcCap(size_t cap, size_t newSize){
    size_t resCap = cap;
    while (resCap < newSize){
        resCap = resCap + resCap;
    }
    while (newSize < resCap / 2 && resCap > MIN_CAP){
        resCap /= 2;
    }
    return resCap;
}

void Resize(TVector* v, size_t newSize){
    size_t newCap = CalcCap(v->cap, newSize);
    if (newCap != v->cap){
        v->body = (TElem*)realloc(v->body, newCap*sizeof(TElem));
        for (size_t i = v->cap; i < newCap; i++){
            v->body[i].value = new string;
        }
        v->cap = newCap;
    }
    v->size = newSize;
}

void PrintV(TVector* v){
    for (size_t i = 0; i < v->size; ++i)
        cout << v->body[i].key << '\t' << *v->body[i].value << '\n';
}

void DestroyV(TVector* v){
    for (size_t i = 0; i < v->size; i++){
        delete v->body[i].value;
    }
    free(v->body);
    free(v);
}

TVector* CountingSort(TVector* v, size_t maxKey, size_t minKey){
    TIntVector* tmp = CreateIntv(maxKey + 1, minKey);
    TVector* res = Create();
    size_t i, num;

    SetSize(res, v->size);

    for (i = 0; i < v->size; ++i){
        tmp->body[v->body[i].key]++;
    }
    num = tmp->body[minKey];
    for (i = minKey + 1; i <= maxKey; ++i){
        if (tmp->body[i] != 0){
            tmp->body[i] = tmp->body[i] + num;
            num = tmp->body[i];
        }
    }
    for (int j = v->size - 1; j >= 0; --j){
        i = tmp->body[v->body[j].key] - 1;
        res->body[i].key = v->body[j].key;
        res->body[i].value = v->body[j].value;
        tmp->body[v->body[j].key]--;
    }
    free(tmp->body);
    free(tmp);
    return res;
}

int main(){

    TVector* v = Create();
    size_t max = 0;
    size_t min = 65535;
    size_t key;
    size_t b = 0;
    time_t t1, t2, t;

    while (cin >> key) {
        Resize(v, v->size + 1);
        if (cin >> *v->body[v->size - 1].value){
            v->body[v->size - 1].key = key;
        }
        if (key > max)
            max = key;
        if (key < min)
            min = key;
        b = 1;
    }

    if (b == 1){

        t1 = time(NULL);

        v = CountingSort(v, max, min);

        t2 = time(NULL);
        t = t2 - t1;
        cout << "time: " << t << endl;

        //PrintV(v);
    }

    DestroyV(v);

    return 0;
}
