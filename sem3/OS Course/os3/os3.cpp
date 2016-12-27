
#include <iostream>
#include <fstream>
#include <ctime>
#include <stack>
#include <windows.h>
#include <conio.h>
#include <string>

using namespace std;
struct LNUM		//������������ ������� ����� � ���������
{
	unsigned char v[32];
};
struct PARAM	
{
	int beg,n;	//��������� ������ ����� � ������� � ���-�� ����������� �����
};
int maxmem=1024;	//������������ ������ ������
int nth=4;			//���-��� �������
LNUM *arr;			//������ ������� �����
LNUM sum={0},avg={0};	
int numbers=0;		
HANDLE mutex;		


//c=a+b
void add(LNUM *a,LNUM *b,LNUM *c)
{
	unsigned char cf=0;	//������� �� �������� ������� � �������
	for(int i=0;i<sizeof(c->v);i++)	//���� �� �������� ����� �� �������� � ��������
	{
		unsigned int t=a->v[i]+b->v[i]+cf;	//������� ��������� ������� � �������
		
		c->v[i]=t;		
		cf=t>>8;		//��������� �������
		
	}
}

void udiv(LNUM *a,unsigned int b,LNUM *c)
{
	unsigned int ostatok=0;	//������� �� ������� ����� �����
	for(int i=sizeof(a->v)-sizeof(unsigned int);i>=0;i-=4)
	{
		//����� ��������� �������
		unsigned long long t=(unsigned long long)*((unsigned int*)&a->v[i])+(((unsigned long long)ostatok)<<32);
		//��������� ���������
		*((unsigned int*)&c->v[i])=t/b;
		ostatok=t%b;
	}
}

//�����, ����������� ����� �������
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

//�������������� ������-����� � ������� �����
void str2num(char *s, LNUM *n)
{
	char t;
	
	memset(n,0,sizeof(n->v));
	for(;*s;s++)	
	{
		for(int i=sizeof(n->v)-1;i>0;i--)		//�������� ��� ����� ����� �� 4 ����(�������� �� 16)
			n->v[i]=(n->v[i]<<4)|(n->v[i-1]>>4);
		t=*s;	
		if(t>='a'&&t<='f')	
			t-=32;			
		if(t>='A'&&t<='F')	
			t-=7;			
		t-='0';				
		
		n->v[0]=(n->v[0]<<4)|t;	//��������� ����� � ������� ������ �����
	}
	
}
//������������ ����� � ������
void sumsum(int n)
{
	PARAM *param=new PARAM[nth];	
	HANDLE *threads=new HANDLE[nth];	
	int np=nth>n?n:nth;		//���� ���-�� ������ ������, ��� �����, ���������� ���
	int ost=n%np;			//������� ����� ��������� � ������� ������, ����� �������������� ���
	int perth=n/np;			
	int beg=0;				
	for(int i=0;i<np;i++)	
	{
		param[i].beg=beg;	
		param[i].n=i?perth:perth+ost;	
		threads[i]=CreateThread(NULL, 0, thread, (LPVOID)&param[i], 0, NULL);
		beg+=param[i].n;	//������ ����� �������� ��������� �����
	}
	WaitForMultipleObjects(np,threads,TRUE,INFINITE);	
	delete threads;	
	delete param;
}
//����� �������� ����� �� �����
void outnum(LNUM bignum)
{
	stack <char> st;
	char t;
	int j;
	do
	{
		t=bignum.v[0]&15;	//�������� ������� ����� �����
		t+='0';			//������������� �� � ������
		if(t>'9')
			t+=7;
		st.push(t);	//�������� � ����
		//�������� ��� ����� �� 4 ���� ������ (��������� �� 16)
		for(int i=0;i<sizeof(bignum.v)-1;i++)
			bignum.v[i]=(bignum.v[i]>>4)|(bignum.v[i+1]<<4);
		bignum.v[sizeof(bignum.v)-1]=bignum.v[sizeof(bignum.v)-1]>>4;
		//��������� �� ����� ������� 0?
		for(j=0;j<sizeof(bignum.v)&&bignum.v[j]==0;j++);
	}while(j<sizeof(bignum.v));	//���������� ���� �� 0
	while(st.size())	//���� ���� �� ����
	{
		cout << st.top();	//��������� � �������
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
    {//��� ������
		cout << "Can't open"<<file<< endl;	
		system("pause");
		return 1;	//� �����
	}
	int i=0;	
	while(!a.eof())	
	{
		if(i<nnum-1)	
		{
			a >> tmp;	
			if(tmp[0])	
			{
				str2num(tmp,&arr[i]);	//������������� � ���������
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
