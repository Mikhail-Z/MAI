
#include <iostream>
#include <fstream>
#include <ctime>
#include <stack>
#include <windows.h>
#include <conio.h>
#include <string>

using namespace std;
struct LNUM		//«аворачиваем длинное число в структуру
{
	unsigned char v[32];
};
struct PARAM	
{
	int beg,n;	//начальный индекс числа в массиве и кол-во суммируемых чисел
};
int maxmem=1024;	//ћаксимальный размер пам€ти
int nth=4;			// ол-вто потоков
LNUM *arr;			//массив длинных чисел
LNUM sum={0},avg={0};	
int numbers=0;		
HANDLE mutex;		


//c=a+b
void add(LNUM *a,LNUM *b,LNUM *c)
{
	unsigned char cf=0;	//перенос из младшего разр€да в старший
	for(int i=0;i<sizeof(c->v);i++)	//цикл по разр€дам числа от младшего к старшему
	{
		unsigned int t=a->v[i]+b->v[i]+cf;	//сложить очередные разр€ды и перенос
		
		c->v[i]=t;		
		cf=t>>8;		//вычислить перенос
		
	}
}

void udiv(LNUM *a,unsigned int b,LNUM *c)
{
	unsigned int ostatok=0;	//остаток от делени€ части числа
	for(int i=sizeof(a->v)-sizeof(unsigned int);i>=0;i-=4)
	{
		//делим очередные разр€ды
		unsigned long long t=(unsigned long long)*((unsigned int*)&a->v[i])+(((unsigned long long)ostatok)<<32);
		//сохран€ем результат
		*((unsigned int*)&c->v[i])=t/b;
		ostatok=t%b;
	}
}

//ѕоток, суммирующий часть массива
DWORD __stdcall thread(LPVOID p)  
{
	LNUM partsum={0};	
	PARAM *pp=(PARAM*)p;
	for(int i=pp->beg;i<pp->beg+pp->n;i++)	
		add(&partsum,&arr[i],&partsum);
	WaitForSingleObject(mutex,INFINITE);	
	add(&sum,&partsum,&sum);
	ReleaseMutex(mutex);
	return 0;
}  

//преобразование строки-числа в длинное число
void str2num(char *s, LNUM *n)
{
	char t;
	
	memset(n,0,sizeof(n->v));
	for(;*s;s++)	
	{
		for(int i=sizeof(n->v)-1;i>0;i--)		//сдвинуть все число влево на 4 бита(умножить на 16)
			n->v[i]=(n->v[i]<<4)|(n->v[i-1]>>4);
		t=*s;	
		if(t>='a'&&t<='f')	
			t-=32;			
		if(t>='A'&&t<='F')	
			t-=7;			
		t-='0';				
		
		n->v[0]=(n->v[0]<<4)|t;	//поставить цифру в младший разр€д числа
	}
	
}
//суммирование чисел в буфере
void sumsum(int n)
{
	PARAM *param=new PARAM[nth];	
	HANDLE *threads=new HANDLE[nth];	
	int np=nth>n?n:nth;		//если кол-во потоко больше, чем чисел, ограничить его
	int ost=n%np;			//сколько чисел добавл€ть к первому потоку, чтобы просуммировать все
	int perth=n/np;			
	int beg=0;				
	for(int i=0;i<np;i++)	
	{
		param[i].beg=beg;	
		param[i].n=i?perth:perth+ost;	
		threads[i]=CreateThread(NULL, 0, thread, (LPVOID)&param[i], 0, NULL);
		beg+=param[i].n;	//откуда будет начинать следующий поток
	}
	WaitForMultipleObjects(np,threads,TRUE,INFINITE);	
	delete threads;	
	delete param;
}
//вывод большого числа на экран
void outnum(LNUM bignum)
{
	stack <char> st;
	char t;
	int j;
	do
	{
		t=bignum.v[0]&15;	//выделить младшую цифру числа
		t+='0';			//преобразовать ее в символ
		if(t>'9')
			t+=7;
		st.push(t);	//записать в стек
		//—двинуть все число на 4 бита вправо (разделить на 16)
		for(int i=0;i<sizeof(bignum.v)-1;i++)
			bignum.v[i]=(bignum.v[i]>>4)|(bignum.v[i+1]<<4);
		bignum.v[sizeof(bignum.v)-1]=bignum.v[sizeof(bignum.v)-1]>>4;
		//ѕроверить от числа осталс€ 0?
		for(j=0;j<sizeof(bignum.v)&&bignum.v[j]==0;j++);
	}while(j<sizeof(bignum.v));	//продолжаем пока не 0
	while(st.size())	//пока стек не пуст
	{
		cout << st.top();	//извлекаем и выводим
		st.pop();
	}
}
int main(int argc, char *argv[])
{
	
	char file[256];
	
	if(argc>1)	
	{
		char tmp[256];
		for(int i=1;i<argc;i++)	
		{
			strcpy_s(tmp, argv[i]);
			if (memcmp(tmp, "/maxmem=", 8) == 0)	
				sscanf(&tmp[8],"%d",&maxmem);	
			if(memcmp(tmp,"/maxthread=",11)==0)
				sscanf(&tmp[11],"%d",&nth);
		}
	}
	cout << "Enter name of file (in.txt by default)" << endl;
	if (!(cin >> file))
		strcpy(file, "in.txt");
	char tmp[256];
	if(nth>MAXIMUM_WAIT_OBJECTS)	
		nth=MAXIMUM_WAIT_OBJECTS;
	mutex=CreateMutex(NULL,FALSE,NULL);
	int nnum=maxmem/32;
	cout << "maxmem=" << maxmem << endl;
	if(nnum<3)	
	{
		cout << "Not enough memory." << endl;	
		system("pause");
		return 1;	
	}
	arr=new LNUM[nnum];	
	memset(tmp,0,sizeof(tmp));

	fstream a(file, ios::in);
	
    if (a.fail())
    {//при ошибке
		cout << "Can't open"<<file<< endl;	
		system("pause");
		return 1;	//и выйти
	}
	int i=0;	
	while(!a.eof())	
	{
		if(i<nnum-1)	
		{
			a >> tmp;	
			if(tmp[0])	
			{
				str2num(tmp,&arr[i]);	//преобразовать и запомнить
				numbers++;
				i++;
			}
		}
		else	
		{
			sumsum(i);	
			i=0;	
		}
	}
	if(i)	
		sumsum(i);	
	a.close();
	delete arr;
	CloseHandle(mutex);
	cout << "Sum:     ";
	outnum(sum);	
	cout << endl;
	udiv(&sum,numbers,&avg);	
	cout << "Average: ";
	outnum(avg);	
	cout << endl;
	system("pause");
	return 0;
}
