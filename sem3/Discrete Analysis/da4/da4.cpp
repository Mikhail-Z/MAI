#include <iostream>
#include "stdio.h"
#include <cstdlib>
#include <cctype>

const int min_cap = 8;

struct Vector {
    char *letters;
    int size;
    int capacity;
};

void Create(Vector *v) {
    v->letters = (char*)malloc(sizeof(char)*min_cap);
    v->size = 0;
    v->capacity = min_cap;
}

void Push (Vector *v, char c){
    if (v->size + 2 > v->capacity) {
        v->capacity*=2;
        if (!(v->letters = (char*)realloc(v->letters, v->capacity*sizeof(char))))
            perror("ERROR:");
    }
    v->size++;
    v->letters[v->size - 1] = c;
    v->letters[v->size] = '\0';
}

void Destroy(Vector *v) {
    free(v->letters);
    v->size = 0;
    v->capacity = 0;
}

int *Preprocessing (Vector *pattern, int *new_sp) {
    new_sp[0] = 0;
    int i,j;
    for(i=1,j=0;i<pattern->size;i++)
    {
        while(j>0 && pattern->letters[j]!=pattern->letters[i])
            j = new_sp[j-1];
        if(pattern->letters[j]==pattern->letters[i])
            j++;
        new_sp[i]=j;
    }
    return new_sp;
}

struct position {
    int line;
    int col;
};

struct item {
    position pos;
    item *next;
};

struct list {
    item *head;
    item *tail;
    int size;
};

void Create2(list *l) {
    l->head = l->tail = NULL;
    l->size = 0;
}

void Push2(list *l, position p) {
        if (l->size!=0) {
        //std::cout<<73<<std::endl;
        l->tail->next = (item*)malloc(sizeof(item));
        //std::cout<<75<<std::endl;
        l->tail->next->pos = p;
        //std::cout<<77<<std::endl;
        l->tail = l->tail->next;
        //std::cout<<79<<std::endl;
    }
    else {
            //std::cout<<83<<std::endl;
        l->head = (item*)malloc(sizeof(item));
        //std::cout<<85<<std::endl;
        l->head->pos = p;
        //std::cout<<87<<std::endl;
        l->tail = l->head;
        //std::cout<<89<<std::endl;
    }
    l->size++;
}

void Delete_first_item(list *l) {
    if (l->head == l->tail)
        return;
    item *tmp = l->head;
    l->head = l->head->next;
    free(tmp);
    l->size--;
}

void Destroy2(list *l) {
    item *tmp;
    while(l->size!=0) {
        tmp = l->head;
        l->head = l->head->next;
        l->size--;
        free(tmp);
    }
    free(l->head);
    l->head = l->tail;
    l->size = 0;
}


void KMP (Vector *pattern, int *new_sp) {
    //std::cout<<pattern->letters<<std::endl;
    char c;
    int j = 0;
    position p;
    p.col = 0;
    list l;
    Create2(&l);
    int tmp1,tmp2, newflag = 0;
    p.line = 0;
    int flag = 0;
    while((c = getchar())!=EOF) {
        //std::cout<<flag<<std::endl;

        if (c == '\n') {
            p.col++;
            //Push2(&l,p);
            if (l.size > pattern->size) {
                //std::cout<<132<<std::endl;
                Delete_first_item(&l);
            }
            p.line++;
            p.col = 0;
            continue;
        }

        else if (c == '\t' || c == ' ') {
            //std::cout<<flag<<std::endl;
            if (flag !=1 ) {
                p.col++;
                flag = 1;
                if (l.size > pattern->size) {
                    Delete_first_item(&l);
                }
            }
            continue;
        }
        else {
            flag = 0;
            Push2(&l,p);
            if (l.size > pattern->size) {
                Delete_first_item(&l);
            }
            while(j>0 && tolower(pattern->letters[j])!=tolower(c)) {
                j=new_sp[j-1];
            }
            if(tolower(pattern->letters[j])==tolower(c)) {
                j++;
            }
            if (j==pattern->size) {
                if (newflag == 0) {
                    std::cout<<l.head->pos.line + 1<<", "<<l.head->pos.col + 1<<std::endl;
                    tmp1 = l.head->pos.line;
                    tmp2 = l.head->pos.col;
                    newflag = 1;
                }
                else {
                    if (l.head->pos.line != tmp1 || l.head->pos.col != tmp2) {
                        std::cout<<l.head->pos.line + 1<<", "<<l.head->pos.col + 1<<std::endl;
                        tmp1 = l.head->pos.line;
                        tmp2 = l.head->pos.col;
                    }
                }
                j=new_sp[j-1];
            }
        }
    }
    Destroy2(&l);
}

int main() {
    Vector v;
    Create(&v);
    char c;
    while((c = getchar())!='\n') {
        if (c!=' ' && c!= '\t')
            Push(&v, c);
    }
    int *new_sp = (int*)malloc(sizeof(int)*v.size);
    Preprocessing(&v, new_sp);
    //std::cout<<v.size<<std::endl;
    KMP(&v,new_sp);
    //std::cout<<"yes!"<<std::endl;
    free(new_sp);
    Destroy(&v);
}
