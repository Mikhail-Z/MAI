#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int ALPHA = 28;
                                 
char *s;
int countV = 0;
int n;
int lenT, lenR;
int *d, *d2;
int *lPath, *rPath;
int curPos = 0;

struct Vector
{
    int *str;
    int size;
    int capacity;
};

void init(struct Vector *v)
{
    v->size = 0;
    v->capacity = 1;
    v->str = (int*) malloc(v->capacity * sizeof(int));
}

void resize(struct Vector *v)
{    
    v->capacity *= 2;
    int *newStr = (int*) malloc(v->capacity * sizeof(int));
    int i;
    for (i = 0; i < v->size; i++)
        newStr[i] = v->str[i];
    free(v->str);
    v->str = newStr;
}

void destroy(struct Vector *v)
{
    free(v->str);
    v->size=0;
    v->capacity=0;
}
void add(struct Vector *v, int c)
{
    if (v->size == v->capacity)
        resize(v);
    v->str[v->size++] = c;
}

int getNum(char c)
{
    if (c >= 'a' && c <= 'z')
        return c - 'a';
    if (c >= 'A' && c <= 'Z')
        return c - 'A' + 26;
    if (c == '#')
        return 26;
    if (c == '$')
        return 27;
    return -1;
}

struct Node
{
    int L, R;
    int pr;
    int suf;
    struct Vector *usedSymbols;
    struct Vector *children;
};

struct Node *nodes;

void initNode(struct Node *node, int L, int R, int pr, int suf)
{
    node->L = L;
    node->R = R;
    node->pr = pr;
    node->suf = suf;
    node->usedSymbols = (struct Vector*) malloc(sizeof(struct Vector));
    node->children = (struct Vector*) malloc(sizeof(struct Vector));
    init(node->usedSymbols);
    init(node->children);
}

void addChild(struct Node *node, int c, int childNumber)
{
    int i;
    for (i = 0; i < node->usedSymbols->size; i++)
        if (node->usedSymbols->str[i] == c)
        {
            node->children->str[i] = childNumber;
            return;
        }
    add(node->usedSymbols, c);
    add(node->children, childNumber);
}

int get(struct Node *node, int c)
{
    int i;
    for (i = 0; i < node->usedSymbols->size; i++)
        if (node->usedSymbols->str[i] == c)
            return node->children->str[i];
    return -1;
}

int length(struct Node *node)
{
    return node->R - node->L;
}

struct Pos
{
    int v;
    int len;
};

struct Pos *cur = NULL;

void initPos(struct Pos *pos, int v, int len)
{
    pos->v = v;
    pos->len = len;
}


struct Pos* newPos(int v, int len)
{
    struct Pos *pos = (struct Pos*) malloc(sizeof(struct Pos));
    pos->v = v;
    pos->len = len;
    return pos;
}


void calcSuf(int v);

inline int getSuf(int v)
{
    if (nodes[v].suf == -1)
        calcSuf(v);
    return nodes[v].suf;
}

void branchFromVertex(int v, int k) 
{
    int newV = countV++;
    initNode(&nodes[newV], k, n, v, -1);

    addChild(&nodes[v], getNum(s[k]), newV);
}

int split(int v, int len)
{
    int u = nodes[v].pr;
    int newV = countV++;
    int L = nodes[v].L, R = nodes[v].R; 
    initNode(&nodes[newV], L, R - len, u, -1);
    addChild(&nodes[u], getNum(s[L]), newV);
    nodes[v].L = R - len;
    nodes[v].pr = newV;
    addChild(&nodes[newV], getNum(s[R - len]), v); 
    return newV;
}

int branchFromEdge(int v, int len, int k) 
{
    int newV = split(v, len);
    branchFromVertex(newV, k);
    return newV;
}

void calcSuf(int v)
{
    int pr = nodes[v].pr;
    int suf = getSuf(pr);
    int len = length(&nodes[v]);
    int curL = nodes[v].L;
    if (pr == 0)
    {
        len--;
        curL++;
    }
    while (len > 0)
    {
        int next = get(&nodes[suf], getNum(s[curL]));
        if (length(&nodes[next]) > len)
            break;
        len -= length(&nodes[next]); 
        curL += length(&nodes[next]);
        suf = next;
    }
    if (len == 0)
    {
        nodes[v].suf = suf;
        return;
    } 
    int next = get(&nodes[suf], getNum(s[curL]));
    int newV = split(next, length(&nodes[next]) - (nodes[v].R - curL)); 
    nodes[v].suf = newV;
}

struct Pos* go(int v, int k)
{
    int u = get(&nodes[v], getNum(s[k]));  
    if (u != -1)
    {
        free(cur);
        return newPos(u, length(&nodes[u]) - 1); 
    }
    branchFromVertex(v, k);
    if (v == 0)
    {
        free(cur);
        return newPos(v, 0);
    }
    return go(getSuf(v), k); 
}

void addSymbol(int k)
{
    int u = cur->v;
    int len = cur->len;
    if (len == 0)
    {
        cur = go(u, k);
        return;
    }
    else if (s[nodes[u].R - len] == s[k])
    {
        free(cur);
        cur = newPos(u, len - 1);
        return;
    } 
    int newV = branchFromEdge(u, len, k);
    cur = go(getSuf(newV), k);
}

int max(int a, int b)
{
    if (a < b)
        return b;
    return a;
}

void dfs(int v, int len, int *maxLen)
{
    int cnt = 0;
    int curLen = len + length(&nodes[v]);
    d[v] = d2[v] = 0;
    int i;
    for (i = 0; i < ALPHA; i++)
    {
        int next = get(&nodes[v], i);
        if (next != -1)
        {
            dfs(next, curLen, maxLen);
            cnt++;
            d[v] = max(d[v], d[next]);
            d2[v] = max(d2[v], d2[next]);
        }
    }
    if (!cnt)
    {
        if (curLen > lenT + 2)
            d[v] = 1;
        if (curLen > 1 && curLen <= lenT + 1)
            d2[v] = 1;
    }
    if (d[v] == 1 && d2[v] == 1 && curLen >= *maxLen)
        *maxLen = curLen;
}          

void getAnswer(int v, int len, int maxLen)
{
    int curLen = len + length(&nodes[v]);
    if (curLen == maxLen && d[v] && d2[v])
    {
        int i, j;
        for (i = 0; i < curPos; i++)
            for (j = lPath[i]; j < rPath[i]; j++)
                printf("%c", s[j]);
        puts("");   
    }
    int i;
    for (i = 0; i < ALPHA; i++)
    {
        int next = get(&nodes[v], i);
        if (next != -1)
        {
            lPath[curPos] = nodes[next].L;
            rPath[curPos++] = nodes[next].R;
            getAnswer(next, curLen, maxLen);
            curPos--;
        }
    }
}
   
int main() 
{
    struct Vector r, t;
    init(&r);
    init(&t);

    char c = getchar();    
    while (c != '\n')
    {
        add(&r, (int) c);
        c = getchar();
    }
    lenR = r.size;

    c = getchar();    
    while (c != '\n')
    {
        add(&t, (int) c);
        c = getchar();
    }
    lenT = t.size;
    

    n = 0;
    s = (char*) malloc(lenR + lenT + 2);
    int i;
    for (i = 0; i < lenR; i++)
        s[n++] = r.str[i];
    s[n++] = '#';
    for (i = 0; i < lenT; i++)
        s[n++] = t.str[i];
    s[n++] = '$';
    
    /*destroy(&r);
    destroy(&t);*/

    nodes = (struct Node*) malloc(sizeof(struct Node) * (3 * n));

    cur = newPos(0, 0);
    initNode(&nodes[countV++], 0, 0, 0, 0);    
    
    for (i = 0; i < n; i++)
        addSymbol(i);

    d = (int*) malloc(sizeof(int) * (countV));
    d2 = (int*) malloc(sizeof(int) * (countV));
    lPath = (int*) malloc(sizeof(int) * (countV));
    rPath = (int*) malloc(sizeof(int) * (countV));
    
    int maxLen = 0;
    free(cur);
    dfs(0, 0, &maxLen);
    printf("%d\n", maxLen);
    getAnswer(0, 0, maxLen);

    return 0;
}
