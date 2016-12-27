#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <locale.h>
#include <conio.h>

#define DELIMITERS  " .,:;?!\n\r\t" 

char file[MAX_PATH]={0};

DWORD minsize=0,maxsize=1000000,maxmem=1000000;
char *cmd;	
HANDLE heap;

//Обрезание пробелов с обеих сторон строки
void alltrim(char *str)
{
	int i;
	for(i=lstrlen(str)-1;i>=0&&(str[i]==' '||str[i]=='\t'||str[i]=='\n');i--)str[i]=0;	//Замена крайних пробелов с правой стороны нулями
	for(i=0;str[i]!=0&&(str[i]==' '||str[i]=='\t');i++);		//Подсчет кол-ва пробелов с левой стороны строки
	if(i>0)	memmove(str,&str[i],lstrlen(&str[i])+1);	//если более 0 пробелов, сдвинуть строку
}


void exit()
{
	HeapFree(heap,NULL,cmd);	
	ExitProcess(0);
}
//подсказка
void help()
{
	printf("? - Эта подсказка.\n");
	printf("help - Эта подсказка.\n");
	printf("exit - Выход.\n");
	printf("file=f - Установить для обработки файл f.\n");
	printf("Пример: file=test.txt\n");
	printf("minsize=n - Установить минимальный размер обрабатываемого файла в n.\n");
	printf("Пример: minsize=10\n");
	printf("maxsize=n - Установить максимальный размер обрабатываемого файла в n.\n");
	printf("Пример: maxsize=1000\n");
	printf("readstr=n - Прочитать из файла строку с номером n.\n");
	printf("Пример: readstr=3\n");
	printf("searchbeg=s - Поиск слов, начинающихся на подстроку s.\n");
	printf("Пример: searchbeg=lo\n");
	printf("searchend=s - Поиск слов, заканчивающихся на подстроку s.\n");
	printf("Пример: searchend=tt\n");
	printf("searchall=s - Поиск слов, содержащих подстроку s в любом месте.\n");
	printf("Пример: searchall=big\n");
	printf("del=pos,size - Удаление из файла фрагмента, начинающегося со смещения pos(начинается с 0) длиной size.\n");
	printf("Пример: del=10,3\n");
	printf("write=pos,s - Запись в файла фрагмента s, начинающегося со смещения pos(начинается с 0).\n");
	printf("Пример: write=10,abc\n");
	printf("maxmem=n - Установить максимальный размер выделяемой памяти в n.\n");
	printf("Пример: maxmem=1000\n");
	printf("stat - Вывод кол-ва строк и символов в файле.\n");
}
void setminsize(char *param)
{
	DWORD tmp;
	alltrim(param);			
	if(sscanf(param,"%u",&tmp)!=1)	
	{	
		printf("Wrong value %s.\n",param);	
	}
	else
		minsize=tmp;	
}
void setmaxsize(char *param)
{
	DWORD tmp;
	alltrim(param);			
	if(sscanf(param,"%u",&tmp)!=1)	
	{	
		printf("Wrong value %s.\n",param);	
	}
	else
		maxsize=tmp;	
}
void setmaxmem(char *param)
{
	DWORD tmp;
	alltrim(param);			
	if(sscanf(param,"%u",&tmp)!=1||tmp==0)	
	{	
		printf("Wrong value %s.\n",param);	
	}
	else
		maxmem=tmp;		
}
//Вывод состояния файла (количество строк и символов в файле)
void stat()
{
	DWORD fsize,r;
	HANDLE hfile;	
	char *txt;		
	if(file[0]==0)	
	{
		printf ("Select file first\n");	
		return;							
	}
	hfile=CreateFile(file,GENERIC_READ,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL); // открытие файла на чтение
	if(hfile==INVALID_HANDLE_VALUE)				
	{
		printf("Error opening file %s.\n",file);
		return;									
	}
	fsize=GetFileSize(hfile,NULL);		
	txt=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,maxmem);
	int dop=0;	
	int str=0;		
	DWORD i;
	do
	{
		ReadFile(hfile,txt,maxmem,&r,NULL);					
		for(i=0;i<r;i++)	
			if(txt[i]=='\n')	
			{
				str++;	//увеличить кол-во строк
				dop=0;	//сбросить признак наличия символов в строке
			}
			else
				dop=1;	//иначе в строке есть как минимум один символ
	}
	while(r);
	CloseHandle(hfile);
	int chnum;
	chnum = (txt[i] == '\n') ? fsize - ((str + 1) * 2) : fsize - (str * 2);
	str=str+dop;	//если в последней строке есть хоть один символ, увеличиь кол-во строк
	printf("In file %s %d strings and %d characters.\n",file,str,chnum);
	HeapFree(heap,0,txt);	
}

//Прочитать конкретную строку из файла 
void readstr(char *param)
{
	DWORD tmp,r;
	HANDLE hfile;		
	char *txt;			
	alltrim(param);			
	if(file[0]==0)	
	{
		printf ("Select file first\n");	
		return;							
	}

	if(sscanf(param,"%u",&tmp)!=1)	
	{	
		printf("Wrong value %s.\n",param);	
		return;								
	}
	if(tmp==0)	//если введен 0
	{
		printf("Wrong value %s.\n",param);	
		return;								
	}
	hfile=CreateFile(file,GENERIC_READ,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL); // открытие файла на чтение
	if(hfile==INVALID_HANDLE_VALUE)				
	{											
		printf("Error opening file %s.\n",file);
		return;									
	}
	txt=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,maxmem);
	DWORD str=1;	
	bool fnd=false;	
	do
	{
		ReadFile(hfile,txt,maxmem,&r,NULL);					
		for(DWORD i=0;i<r;i++)	//идем по прочитанному
		{
			if(str==tmp&&txt[i]!='/r') 
			{
				printf("%c",txt[i]);	
				fnd=true;	
			}
			if(txt[i]=='\n')	
			{
				str++;	
			}
			if(str>tmp)
				break;
		}
	}
	while(r);
	CloseHandle(hfile);									
	if(!fnd)	
	{	
		printf("String not exist.\n");
	}
	HeapFree(heap,0,txt);	
}


//Запись любого количества символов с любой позиции в файле
void write(char *param)
{
	DWORD fsize,rw,pos,size;
	HANDLE hfile;	
	char *ins;		
	char *txt;		
	if(file[0]==0)	
	{
		printf ("Select file first\n");	
		return;							
	}
	//если в конце параметра перевод строки, удалить его
	if(param[lstrlen(param)-1]=='\n')param[lstrlen(param)-1]=0;
	
	ins=strchr(param,',');
	if(ins==NULL)	
	{
		printf("Wrong value %s.\n",param);	
		return;								
	}
	(*ins++)=0;	
	if(sscanf(param,"%d",&pos)!=1)	
	{	
		printf("Wrong value %s.\n",param);	
		return;								
	}
	hfile=CreateFile(file,GENERIC_READ|GENERIC_WRITE,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL); // открытие файла на чтение
	if(hfile==INVALID_HANDLE_VALUE)				
	{											
		printf("Error opening file %s.\n",file);
		return;									
	}
	fsize=GetFileSize(hfile,NULL);
	size=lstrlen(ins);	
	
	if(pos>fsize)		//если позиция выходит за границу файла
	{
		printf("Wrong position.\n");	
		return;							
	}
	txt=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,maxmem);	
	SetFilePointer(hfile,0,NULL,FILE_END);	
	for(int i=0;i<size;i++)				
		WriteFile(hfile,txt,1,&rw,NULL);
	DWORD rptr=fsize,rws,wptr=fsize+size;	
	while(rptr!=pos)	//продолжаем сдвигать пока не достигли нужной позиции
	{
		rws=rptr;	//запоснить прошлое значение
		if(maxmem>rptr||rptr-maxmem<pos)	//если весь фрагнмент помещается в память
			rptr=pos;		
		else
			rptr=rptr-maxmem;	
		rws-=rptr;	
		wptr-=rws;	
		SetFilePointer(hfile,rptr,NULL,FILE_BEGIN);			
		ReadFile(hfile,txt,rws,&rw,NULL);							
		SetFilePointer(hfile,wptr,NULL,FILE_BEGIN);		
		WriteFile(hfile,txt,rws,&rw,NULL);							
	}
	SetFilePointer(hfile,pos,NULL,FILE_BEGIN);		
	WriteFile(hfile,ins,size,&rw,NULL);							
	CloseHandle(hfile);											
	HeapFree(heap,0,txt);	

}

//удаление любого количества символов с любой позиции в файле
void del(char *param)
{
	DWORD fsize,rw,pos,size;
	HANDLE hfile;	
	char *txt;		
	alltrim(param);			
	if(file[0]==0)	
	{
		printf ("Select file first\n");	
		return;							
	}
	if(sscanf(param,"%d,%d",&pos,&size)!=2)	
	{	
		printf("Wrong value %s.\n",param);	
		return;								
	}
	hfile=CreateFile(file,GENERIC_READ|GENERIC_WRITE,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL); // открытие файла на чтение
	if(hfile==INVALID_HANDLE_VALUE)				
	{											
		printf("Error opening file %s.\n",file);
		return;									
	}
	txt=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,maxmem);
	fsize=GetFileSize(hfile,NULL);	
	
	if(pos>fsize)		
	{
		printf("Wrong position.\n");	
		return;							
	}
	if(pos+size>fsize)
	{
		printf("Wrong size.\n");	
		return;						
	}
	DWORD rptr=pos+size,wptr=pos;	//указатели записи и чтения
	do
	{
		SetFilePointer(hfile,rptr,NULL,FILE_BEGIN);		
		ReadFile(hfile,txt,maxmem,&rw,NULL);						
		SetFilePointer(hfile,wptr,NULL,FILE_BEGIN);		
		WriteFile(hfile,txt,rw,&rw,NULL);							
		rptr+=rw;	//увеличить указатели
		wptr+=rw;
	}while(rw);	//продолжаем пока не закончился файл
	SetEndOfFile(hfile);	//обрезать ненужные байты
	CloseHandle(hfile);									
	HeapFree(heap,0,txt);
}

//1 - по началу
//2 - по суффиксу
//3 - по всему слову
void search(int type,char *samp)
{
	DWORD r;
	HANDLE hfile;		
	char *txt,word[256];	
	int i,j;
	if(file[0]==0)	
	{
		printf ("Select file first\n");	
		return;							
	}
	hfile=CreateFile(file,GENERIC_READ,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL); // открытие файла на чтение
	if(hfile==INVALID_HANDLE_VALUE)					
	{												
		printf("Error opening file %s.\n",file);	
		return;										
	}
	alltrim(samp);			
	txt=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,maxmem);
	j=0;	
	bool wrd=false;	
	r=maxmem;
	for(i=maxmem;;i++)	
	{
		printf("j=%d\n", j);
		if(i==r)	//если конца прочитанного 
		{
			ReadFile(hfile,txt,maxmem,&r,NULL);					
			if(!r)		//если файл закончился
			{
				if(wrd)	//если открыто слово
				{
					printf("! %s\n",word);

					word[j]=0;
					
					if(lstrlen(word)>=lstrlen(samp))	//но только если длина слова не меньше длины искомой строки
					{
						if(type==3&&strstr(word,samp))	//если найден в любом месте слова
						{
							//вывести это слово
							printf("%s\n",word);
						}
						if(type==1&&memcmp(word,samp,lstrlen(samp))==0)	//если найден с начала слова
						{
							//вывести это слово
							printf("%s\n",word);
						}
						if(type==2&&strcmp(&word[lstrlen(word)-lstrlen(samp)],samp)==0)	//если найден с конца слова
						{
							//вывести это слово
							printf("%s\n",word);
						}
					}
				}
				break;	//когда файл закончился выходим из цикла
			}
			i=0;	
		}
		if(strchr(DELIMITERS,txt[i])&&wrd)	//если закончилось слово, поиск в нем
		{
			wrd=false;
			word[j]=0;
			j=0;	
			
			if(lstrlen(word)>=lstrlen(samp))	
			{
				if(type==3&&strstr(word,samp))	
				{
					//вывести это слово
					printf("%s\n",word);
				}
				if(type==1&&memcmp(word,samp,lstrlen(samp))==0)
				{
					//вывести это слово
					printf("%s\n",word);
				}
				if(type==2&&strcmp(&word[lstrlen(word)-lstrlen(samp)],samp)==0)	
				{
					//вывести это слово
					printf("%s\n",word);
				}
			}
		}
		if(!strchr(DELIMITERS,txt[i]))	
		{
			wrd=true;	
			word[j]=txt[i];	
			j++;
		}



	}
	CloseHandle(hfile);									
	HeapFree(heap,0,txt);	
}
//Функция смены файла, не закрывая приложение текстового процессора
void setfile(char *name)
{
	WIN32_FIND_DATA ffd;
	HANDLE hFind;
	alltrim(name);			
	hFind = FindFirstFile(name,&ffd);	
	if(hFind==INVALID_HANDLE_VALUE)			
	{										
		printf ("File %s not found\n",name);
		return;								
	} 
    FindClose(hFind);		
	if(ffd.nFileSizeHigh)		
	{
		printf ("File too large\n");	
		return;							
	}
	if(ffd.nFileSizeLow>maxsize)	
	{
		printf ("File too large\n");	
		return;							
	}
	if(ffd.nFileSizeLow<minsize)	
	{
		printf ("File too small\n");	
		return;							
	}
	lstrcpy(file,name);		
}
//Выполнение команды
void exec(char *com)
{
	int i;
	char cc[256];
	for(i=0;com[i]&&com[i]!='=';i++)	
		cc[i]=com[i];
	cc[i]=0;	
	alltrim(cc);			
	if(cc[0])	
	{
		
		if(lstrcmp(cc,"exit")==0)		
			exit();
		
		else if(lstrcmp(cc,"file")==0&&com[i])
			setfile(&com[i+1]);
		else if(lstrcmp(cc,"minsize")==0&&com[i])
			setminsize(&com[i+1]);
		else if(lstrcmp(cc,"maxsize")==0&&com[i])
			setmaxsize(&com[i+1]);
		else if(lstrcmp(cc,"maxmem")==0&&com[i])
			setmaxmem(&com[i+1]);
		else if(lstrcmp(cc,"readstr")==0&&com[i])
			readstr(&com[i+1]);
		else if(lstrcmp(cc,"searchbeg")==0&&com[i])
			search(1,&com[i+1]);
		else if(lstrcmp(cc,"searchend")==0&&com[i])
			search(2,&com[i+1]);
		else if(lstrcmp(cc,"searchall")==0&&com[i])
			search(3,&com[i+1]);
		else if(lstrcmp(cc,"del")==0&&com[i])
			del(&com[i+1]);
		else if(lstrcmp(cc,"write")==0&&com[i])
			write(&com[i+1]);
		else if(lstrcmp(cc,"stat")==0)
			stat();
		else if(lstrcmp(cc,"help")==0)
			help();
		else if(lstrcmp(cc,"?")==0)
			help();
		else	
			printf("Unknown command %s\n",com);
	}
}

int main()
{
	char *c,cmd1[256];
	setlocale(LC_ALL,"Russian");
	heap=GetProcessHeap();	
	c=GetCommandLine();		
	cmd=(char*)HeapAlloc(heap,HEAP_ZERO_MEMORY,lstrlen(c)+1);	//выделить память под командную строку
	lstrcpy(cmd,c);	
	char *p=strchr(cmd,'/');	
	char *pch;
	
	if(p)
	{
		pch=strtok(p,"/");	
		while(pch)			
		{
			exec(pch);		
			pch=strtok(NULL,"/");	
		}
		getch();	
		exit();		
	}
	else
	{
		printf("Interactive mode ready.\nEnter commands.\n");
		while(1)
		{
			fgets(cmd1,256,stdin);	
			exec(cmd1);	
		}
	}
	return 0;
}
