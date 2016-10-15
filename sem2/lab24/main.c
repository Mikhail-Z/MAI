#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include "stack.h"

typedef struct _Node
{
    char _varOp;
    int _num;
    struct _Node *_left;
    struct _Node *_right;
} Node;

Node *treeNodeCreate(void)
{
    Node *tmpNode = (Node *)malloc(sizeof(Node));

    tmpNode->_varOp = '\0';
    tmpNode->_num = 0;
    tmpNode->_left = NULL;
    tmpNode->_right = NULL;

    return tmpNode;
}

void treeDestroy(Node **node)
{
    if (*node == NULL)
        return;

    if ((*node)->_left != NULL)
        treeDestroy(&(*node)->_left);

    if ((*node)->_right != NULL)
        treeDestroy(&(*node)->_right);

    free(*node);

    *node = NULL;
}

int isNumber(const char ch)
{
    return (ch >= '0' && ch <= '9');
}

int isLetter(const char c)
{
    return (c>='a' && c<='z' || c>='A' && c<='Z');
}

int isOperation(const char c)
{
    return (c=='-' || c=='+' || c=='*' || c=='/' || c=='^');
}
int priority(const char op)
{
    if (op=='^') return 4;
    if (op=='*' || op=='/') return 3;
    if (op=='-' || op=='+') return 2;
    else return 1;
}

int OldHasBiggerPriority(const char op1, const char op2)
{
    if (op1=='(' && (op2=='(') || op2 ==')') return 0;
    if (op1=='^' && op2=='^') return 0;
    return (priority(op1)>=priority(op2));
}

void PKL(Node **node, const int level)
{
    if (*node == NULL)
        return;

    if ((*node)->_right != NULL)
        PKL(&(*node)->_right, level + 1);

    if ((*node)->_varOp != '\0')
        printf("%*s%c\n", level * 4, "", (*node)->_varOp);
    else
        printf("%*s%d\n", level * 4, "", (*node)->_num);

    if ((*node)->_left != NULL)
        PKL(&(*node)->_left, level + 1);
}

void postOrder(const char *str, Stack *st)
{
    int i = 0, step = -1, isBracket = 0;
    char tmpCh;
    Token tk;
    Stack stOp;

    stackCreate(&stOp);//создается служебный стек для того

    tk._varOp = '\0';
    tk._num = 0;

    while (str[i] != '\0')
    {
        if (isLetter(str[i]))
        {
            tk._varOp = str[i];

            stackPush(st, tk);
        }
        else if (isNumber(str[i]))
        {
            tk._varOp = '\0';

           // if (!isDot)
                tk._num = tk._num * 10 + str[i] - '0';

            if (!isNumber(str[i + 1])) //определили, что след операнд не константа и не точка
            {
                stackPush(st, tk);

                tk._num = 0;
                step = -1;
            }
        }
        else if (isOperation(str[i]))
        {
            tk._varOp = str[i];

            if (str[i] == ')')
                isBracket = 1;
            else if (str[i] == '-' && (i == 0 || str[i - 1] == '(')) //ситуация, когда (- или -
            {
                tmpCh = tk._varOp;
                tk._varOp = '\0'; //ставим 0 перед минусом
                tk._num = 0;

                stackPush(st, tk);

                tk._varOp = tmpCh;
            }

            while (!stackEmpty(&stOp) && (OldHasBiggerPriority(stackTop(&stOp)._varOp, str[i]) || isBracket)) //сравнение текущей операции с вершиной стека и если в вершине выше приоритет
            {
                if (stackTop(&stOp)._varOp == '(')//просто извлекаем
                    isBracket = 0;
                else
                    stackPush(st, stackTop(&stOp));//переносим в выхлжной стек опреация из служебного стека если приоритет операции на высоте выше нашей

                stackPop(&stOp);
            }

            if (str[i] != ')')    //переносим в стек служебный наше операцию
                stackPush(&stOp, tk);
        }

        i++;
    }

    while (!stackEmpty(&stOp))
    {
        stackPush(st, stackTop(&stOp));
        stackPop(&stOp);
    }

    stackDestroy(&stOp);
}

void treeBuild(Node **node, Stack *st)
{
    Token token;

    if (stackEmpty(st))
        return;

    token = stackTop(st);

    stackPop(st);

    (*node) = treeNodeCreate();
    (*node)->_varOp = token._varOp;
    (*node)->_num = token._num;

    if (isOperation((*node)->_varOp))
    {
        treeBuild(&(*node)->_right, st);   //строит корневой узел и операцию выбирает рекурсивно и содает правй и левый узлы
        treeBuild(&(*node)->_left, st);
    }
}

int treeChange(Node **root, int count)
{
    printf("OK\n");
    //ситуация когда очередная левая вершина - это умножить/разделить
    if ((priority((*root)->_varOp)==3 || priority((*root)->_varOp)==4) && isOperation((*root)->_left->_varOp))
    {
        printf("195\n");
        int sum = treeChange(&(*root)->_left, 0);
        return 0;
    }

    //ситуация, когда конец рекурсии, т.е. в самом низу
    if (isOperation((*root)->_varOp) && (*root)->_left!=NULL && (*root)->_right!=NULL && !isOperation((*root)->_left->_varOp))
    {
        printf("vnizu\n");
        if (isOperation((*root)->_right->_varOp)) { int sum1=treeChange(&(*root)->_right, 0); }
        if ((*root)->_varOp=='+' || (*root)->_varOp=='-' && (*root)->_left->_num==0 && (*root)->_right->_varOp=='\0')
        {
        int sum;
        if ((*root)->_left->_varOp=='\0' && (*root)->_right->_varOp=='\0')
        {
            sum=(*root)->_left->_num + (*root)->_right->_num;
            (*root)->_left=NULL;
            (*root)->_right=NULL;
            (*root)->_num=sum;
            (*root)->_varOp='\0';
            return sum;
        }

        if ((*root)->_left->_varOp=='\0' && (*root)->_right->_varOp!='\0' || (*root)->_left->_varOp!='\0' && (*root)->_right->_varOp=='\0')
        {
            if (count==0) return 0;
            else
            {
                char c;
                if (isLetter((*root)->_left->_varOp)) { c=(*root)->_left->_varOp; sum=(*root)->_right->_num; }
                        else { c=(*root)->_right->_varOp; sum=(*root)->_left->_num; }
                (*root)->_left=NULL;
                (*root)->_right=NULL;
                (*root)->_varOp=c;
                return sum;
           }
        }

        if ((*root)->_left->_varOp!='\0' && (*root)->_right->_varOp!='\0') return 0;
    }
        else {printf("226 %c\n"); return 0;}
    }
    //пока движемся вниз
    if ((*root)!=NULL && (*root)->_left!=NULL &&(*root)->_right!=NULL && isOperation((*root)->_left->_varOp) && isOperation((*root)->_varOp))
    {
        int sum1;
        int sum2;
        if (isOperation((*root)->_right->_varOp)) {sum1=treeChange(&(*root)->_right, 0); printf("sum1 = %d\n", sum1);}
        if ((*root)->_varOp=='+')
        {
            if ((*root)->_right->_varOp=='\0') {
                int c=(*root)->_right->_num;
                printf("root->_right->_num = %d\n", c);
                count++;
                sum2=treeChange(&(*root)->_left, count); printf("sum2_1 = %d\n", sum2); printf("root=%d %c\n",(*root)->_left->_num, (*root)->_left->_varOp); sum2 += (*root)->_right->_num; printf("236\n"); printf("sum2= %d\n",sum2);
                //когда после преобразования и слева и справа числа
                if ((*root)->_left->_varOp=='\0')
                {
                    //if (count==)
                    (*root)->_num=sum2;
                    (*root)->_varOp='\0';
                    (*root)->_left=NULL;
                    (*root)->_right=NULL;
                    printf("245\n");
                    return sum2;
                }
                printf("%d\n", count);
                //когда после преобразования слева буква, а справа число
                if (isLetter((*root)->_left->_varOp)) {
                    if (count>1)
                    {
                        printf("251\n");
                        char c;
                        c=(*root)->_left->_varOp;
                        (*root)->_left=NULL;
                        (*root)->_right=NULL;
                        (*root)->_varOp=c;
                        printf("257\n");
                        return sum2;
                    }
                    else if (count==1)
                    {
                        (*root)->_right->_num=sum2;
                        printf("272\n");
                        return 0;
                    }
                }
                //когда слева операция
                else if (isOperation((*root)->_left->_varOp))
                {
                    if (count==1 && (*root)->_right->_varOp=='\0')
                    {
                        (*root)->_right->_num+=sum2;
                        return 0;
                    }
                    else
                    {
                        printf("265\n");
                        (*root)=(*root)->_left; //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        printf("267\n");
                        return sum2;
                    }
                    //если это минус, то ничего не надо менять
                }
            }
            //если справа буква
            if (isLetter((*root)->_right->_varOp))
            {
                sum2=treeChange(&(*root)->_left, count); printf("270\n"); printf("root1=%d\n", (*root)->_left->_num);
                //если слева число
                if ((*root)->_left->_varOp=='\0')
                {
                    printf("280\n");
                    if (count==0) {printf("281\n"); return 0;}
                    else if (count==1) {(*root)->_left->_num=sum2; (*root)->_left->_varOp='\0'; return 0;}
                    else
                    {
                        char c;
                        printf("285\n");
                        c=(*root)->_right->_varOp;
                        (*root)->_left=NULL;
                        (*root)->_right=NULL;
                        (*root)->_varOp=c;
                        printf("291\n");
                        return sum2;
                   }
                }
                printf("310\n"); return sum2;
            }
            //когда справа операция
            if (isOperation((*root)->_right->_varOp))
            {
                sum2=treeChange(&(*root)->_left, count); printf("315\n");
                printf("327 %c %d\n", (*root)->_left->_varOp, (*root)->_right->_right->_num);
                //когда слева число
                if ((*root)->_left->_varOp=='\0' && count>1)
                {
                    (*root)->_left=(*root)->_right;
                    (*root)->_right=NULL;
                    return sum2;
                }
                else return sum2;
            }

        }
        //если текущая операция не +
        else
        {
            int sum=treeChange(&(*root)->_left, 0);
            printf("301\n");
            return 0;
        }
    }
}

bool treeIsMinusNode(Node **root)
{
    if ((*root)==NULL) return 0;
    if ((*root)->_left==NULL || (*root)->_right==NULL) return 0;
    if ((*root)->_left->_varOp=='\0' && (*root)->_left->_num==0 && (*root)->_varOp=='-')
        return 1;
}

void LKP(Node **root)
{
    if (*root==NULL) return ;
    if ((*root)->_left!=NULL && !treeIsMinusNode((root)))
    {
        if ((*root)->_left->_left!=NULL) printf("(");
        LKP(&(*root)->_left);
        if ((*root)->_left->_left!=NULL) printf(")");
    }

    if ((*root)->_varOp!='\0')
        printf("%c", (*root)->_varOp);
    else
        printf("%d", (*root)->_num);

   if ((*root)->_right!=NULL)
   {
       if ((*root)->_right->_left!=NULL) printf("(");
       LKP(&(*root)->_right);
       if ((*root)->_right->_left!=NULL) printf(")");
   }
}




int main(void)
{
    int action;
    char expr[255];
    Node *root = NULL;
    Stack stPost;

    while (1)
    {
        printf("Menu:\n");
        printf("1) Enter the expression\n");
        printf("2) Print of the first expression\n");
        printf("3) Print of the old tree\n");
        printf("4) Print of the new tree \n");
        printf("5) Exit \n");
        printf("Choose the action ");
        scanf("%d", &action);

        switch (action)
        {
            case 1:
            {
                printf("enter the expression ");
                scanf("%s", expr);

                stackCreate(&stPost);
                postOrder(expr, &stPost);
                treeBuild(&root, &stPost);
                stackDestroy(&stPost);

                break;
            }

            case 2:
            {
                printf("the first expression %s\n", expr);

                break;
            }

            case 3:
            {
                if (root != NULL)
                {
                    printf("the tree of the first expression\n");
                    PKL(&root, 0);
                }
                else
                    printf("the tree of expression is empty\n");

                break;
            }


            case 4:
            {
                if (root != NULL)
                {
                    printf("the tree of new expression\n");
                    int sum = treeChange(&root, 0);
                    PKL(&root, 0);
                }
                else
                    printf("the new tree of expression is empty \n");

                break;
            }

            case 5:
            {
                break;
            }
            default:
            {
                printf("Error. There is no such way\n");

                break;
            }
        }

        if (action == 5)
            break;
    }

    treeDestroy(&root);
    return 0;
}
