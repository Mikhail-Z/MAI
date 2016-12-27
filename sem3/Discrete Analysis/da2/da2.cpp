#include <iostream>
#include <string.h>
#include <iomanip>
#include <locale>

struct Pair {
    char *key;
    unsigned long long int value;
};

struct TNode {
    char *key;
    unsigned long long int value;
    int height;
    TNode *right;
    TNode *left;
};

TNode *TreeDestroy(TNode *root);
void PreOrder(TNode *root, FILE *f);
TNode* RightRotation(TNode *root);
TNode *LeftRotation(TNode *root);
int Height(TNode *root);
void NewHeight(TNode *root);
int BalanceFactor(TNode *root);
TNode *Balance(TNode *root);
TNode *Insert(TNode *root, Pair p);
void Search(TNode *root, char *key);
TNode *SearchMin(TNode *root);
TNode *Delete(TNode *root, char *key);
TNode *DeleteMin(TNode *root);
TNode *Add(TNode *root, Pair p);


int main(void)
{
    char mystring[257];
    int l = 0;
    TNode *root = NULL;
    while (1) {
        Pair tmp;
        if (!(std::cin>>mystring))
            break;
        switch(mystring[0]) {

            case '+':
            {               
                std::cin>>mystring;
                l = strlen(mystring);
                tmp.key = new char [l+1];
                strcpy(tmp.key,mystring);
                std::cin>>tmp.value;
                int i;
                for (i = 0; i <= l; i++)
                    tmp.key[i] = tolower(tmp.key[i]);
                l = strlen(tmp.key);
                root = Insert(root, tmp);
                delete [] tmp.key;
                break;
            }

            case '-':
            {
                mystring[0] = '\0';
                std::cin>>mystring;
                int i;
                for (i=0; i <= strlen(mystring); i++)
                    mystring[i] = tolower(mystring[i]);
                root = Delete(root, mystring);
                break;
            }
            case '!':
                mystring[0] = '\0';
                std::cin>>mystring;
                if (strcmp(mystring,"Save") == 0) {
                    std::cin>>mystring;
                    FILE *f = fopen(mystring, "wb");
                    if (!f)
                        perror("ERROR");
                    PreOrder(root, f);
                    fclose(f);
                    std::cout<<"OK"<<std::endl;
                } else
                    if (strcmp(mystring, "Load")==0) {
                    int len = strlen(mystring);
                    std::cin>>mystring;
                    FILE *f = fopen(mystring, "rb");
                    if (!f)
                        perror("ERROR:");
                    root = TreeDestroy(root);
                    Pair p;
                    while (fread(&len,sizeof(int), 1, f)) {
                        p.key = new char [len+1];
                        if (!fread(p.key, sizeof(char), len, f))
                            perror("ERROR:");
                        if (!fread(&p.value, sizeof(unsigned long long int), 1, f))
                            perror("ERROR:");
                        root = Add(root, p);
                        delete [] p.key;
                    }
                    fclose(f);
                    std::cout<<"OK"<<std::endl;
                } else {
                    std::cout<<"Wrong command!"<<std::endl;
                    break;
                }
                break;

            default:
            {
                int i;
                int l = strlen(mystring);
                for (i = 0; i <= l; i++)
                    mystring[i] = tolower(mystring[i]);

                Search(root, mystring);
                break;
            }
        }
    }
    if (root) {
        root = TreeDestroy(root);
    }
    return 0;
}


TNode *TreeDestroy(TNode *root) {
    if (root) {
        if(root->left) {
        TreeDestroy(root->left);
        }
        if (root->right) {
            TreeDestroy(root->right);
        }
        delete[] root->key;
        delete root;
        root = NULL;
    }
    return root;
}


void PreOrder(TNode *root, FILE *f) {
    if (root){
        int l = strlen(root->key) + 1;
        if (!fwrite(&l, sizeof(int), 1, f))
            perror("ERROR:");
        if (!fwrite(root->key, sizeof(char), l, f))
            perror("ERROR:");
        if (!fwrite(&root->value, sizeof(unsigned long long int), 1, f))
            perror("ERROR:");
        PreOrder(root->left,f);
        PreOrder(root->right,f);
    }
}

void Search(TNode *root, char *key) {
    if (root == NULL){
        std::cout<<"NoSuchWord"<<std::endl;
    }
    else if (strcmp(root->key, key) > 0)
        Search(root->left, key);
    else if (strcmp(root->key, key) < 0)
        Search(root->right, key);
    else std::cout<<"OK: "<<root->value<<std::endl;
}

TNode* RightRotation(TNode *root) {
    TNode *y = root->left;
    root->left = y->right;
    y->right = root;
    NewHeight(root);
    NewHeight(y);
    return y;
}

TNode *LeftRotation(TNode *root) {
    TNode *x = root->right;
    root->right = x->left;
    x->left = root;
    NewHeight(root);
    NewHeight(x);
    return x;
}

int Height(TNode *root) {
    if (root) return root->height;
    else return 0;
}

int BalanceFactor(TNode *root) {
    return Height(root->right) - Height(root->left);
}

void NewHeight(TNode *root){
    int hleft = Height(root->left);
    int hright = Height(root->right);
    root->height=(hleft > hright ? hleft : hright) + 1;
}

TNode *Balance(TNode *root) {
    NewHeight(root);
    if (BalanceFactor(root) == 2) {
        if (BalanceFactor(root->right) < 0)
            root->right = RightRotation(root->right);
        return LeftRotation(root);
    }
    if (BalanceFactor(root) == -2) {
        if (BalanceFactor(root->left) > 0)
            root->left = LeftRotation(root->left);
        return RightRotation(root);
    }

    return root;
}

TNode *Insert(TNode *root, Pair p) {
    if (!root) {
        std::cout<<"OK"<<std::endl;
        root = new TNode;
        root->height = 1;
        root->key = new char[strlen(p.key)+1];
        strcpy(root->key, p.key);
        root->value = p.value;
        root->right = NULL;
        root->left = NULL;
        return root;
    }
    if (strcmp(root->key, p.key) > 0)
        root->left = Insert(root->left, p);
    else if (strcmp(root->key, p.key) < 0)
        root->right=Insert(root->right, p);
    else {
        std::cout<<"Exist"<<std::endl;
        return root;
    }
    return Balance(root);
}

TNode *Add(TNode *root, Pair p) {
    if (!root) {
        root = new TNode;
        root->key = new char[strlen(p.key)+1];
        root->value = p.value;
        strcpy(root->key, p.key);
        root->left = NULL;
        root->right = NULL;
        root->height = 1;
    }
    if (strcmp(root->key,p.key) > 0) {
        root->left=Add(root->left, p);
        root->height = Height(root->left) + 1;
    }
    else  if (strcmp(root->key, p.key) < 0) {
        root->right=Add(root->right, p);
        if (root->left) {
            if ((Height(root->right) + 1) > root->height)
                root->height = Height(root->right) + 1;
            else root->height = Height(root->right) + 1;
        }
    }

    return root;
}

TNode *SearchMin(TNode *root) {
    if (root->left) {
        TNode *t = SearchMin(root->left);
        return t;
    }
    else return root;
}

TNode *Delete(TNode *root, char *key) {
    if (!root) {
        std::cout<<"NoSuchWord"<<std::endl;
        return root;
    }
    if (strcmp(root->key,key) > 0)
        root->left = Delete(root->left, key);
    else if (strcmp(root->key,key) < 0)
        root->right = Delete(root->right, key);
    else {
        TNode *y = root->left;
        TNode *z = root->right;
        delete[] root->key;
        delete root;
        std::cout<<"OK"<<std::endl;
        if (!z) return y;
        TNode* min = SearchMin(z);
        min->right = DeleteMin(z);
        min->left = y;
        return Balance(min);
    }
    return Balance(root);
}



TNode *DeleteMin(TNode *root) {
    if (root->left == 0)
        return root->right;
    root->left = DeleteMin(root->left);
    TNode *t = Balance(root);
    return t;
}
