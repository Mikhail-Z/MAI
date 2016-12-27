#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <thread>
#include <mutex>
#include<math.h>
#define MAXMEM 2000000
int NUMTHREADS;
using namespace std;
mutex infile,outfile, file;
thread_local FILE *ikeys,*ivals,*okeys,*ovals,*tkeys,*tvals;
char *inkeysname=NULL,*invalsname=NULL,*outkeysname=NULL,*outvalsname=NULL;

uint64_t keylen,vallen,n1,n2, nn;

void Merge(uint8_t *keys,uint8_t *vals, uint64_t left, uint64_t right, uint64_t medium, uint64_t keylen,uint64_t vallen )
{
    uint64_t j = left;
    uint64_t k = medium + 1;
    uint64_t count = right - left + 1;

    if (count <= 1) return;

    uint8_t *tmpkeys = new uint8_t[count*keylen];
    uint8_t *tmpvals = new uint8_t[count*vallen];

    for (uint64_t i = 0; i < count; ++i) {
        if (j <= medium && k <= right) {
            if (memcmp(&keys[j*keylen], &keys[k*keylen],keylen)<=0)
            {
                memcpy(&tmpkeys[i*keylen],&keys[j*keylen],keylen);
                memcpy(&tmpvals[i*vallen],&vals[j*vallen],vallen);
                j++;
            }
            else
            {
                memcpy(&tmpkeys[i*keylen],&keys[k*keylen],keylen);
                memcpy(&tmpvals[i*vallen],&vals[k*vallen],vallen);
                k++;
            }
        } else {
            if (j <= medium)
            {
                memcpy(&tmpkeys[i*keylen],&keys[j*keylen],keylen);
                memcpy(&tmpvals[i*vallen],&vals[j*vallen],vallen);
                j++;
            }
            else
            {
                memcpy(&tmpkeys[i*keylen],&keys[k*keylen],keylen);
                memcpy(&tmpvals[i*vallen],&vals[k*vallen],vallen);
                k++;
            }
        }
    }

    j = 0;
    for (uint64_t i = left; i <= right; ++i) {
        memcpy(&keys[i*keylen],&tmpkeys[j*keylen],keylen);
        memcpy(&vals[i*vallen],&tmpvals[j*vallen],vallen);
        j++;

    }
    delete tmpkeys;
    delete tmpvals;
}

void mergefile(uint64_t fst,uint64_t snd,uint64_t fstlen,uint64_t sndlen,uint64_t nmem, uint64_t keylen,uint64_t vallen)
{
    if (fstlen+sndlen <= nmem) return;
    uint64_t r=fst<snd?fst:snd;
    uint64_t i,j;
    uint8_t *akey=new uint8_t[keylen];
    uint8_t *aval=new uint8_t[vallen];
    uint8_t *bkey=new uint8_t[keylen];
    uint8_t *bval=new uint8_t[vallen];
    fseek(okeys,2*sizeof(uint64_t)+r*keylen,SEEK_SET);
    fseek(ovals,2*sizeof(uint64_t)+r*vallen,SEEK_SET);

    fseek(tkeys,2*sizeof(uint64_t)+fst*keylen,SEEK_SET);
    fread(akey,keylen,1,tkeys);
    fseek(tvals,2*sizeof(uint64_t)+fst*vallen,SEEK_SET);
    fread(aval,vallen,1,tvals);

    fseek(tkeys,2*sizeof(uint64_t)+snd*keylen,SEEK_SET);
    fread(bkey,keylen,1,tkeys);
    fseek(tvals,2*sizeof(uint64_t)+snd*vallen,SEEK_SET);
    fread(bval,vallen,1,tvals);

    //cout<<"fst="<<fst<<" fstlen"<<fstlen<<" snd="<<snd<<" sndlen="<<sndlen<<endl;
    for(i=fst,j=snd;i<fst+fstlen&&j<snd+sndlen;)
    {
        if(memcmp(akey, bkey,keylen)<=0 && i<fst+fstlen)
        {
            fwrite(akey,keylen,1,okeys);
            fwrite(aval,vallen,1,ovals);
            i++;
            if(i==fst+fstlen)
                break;
            fseek(tkeys,2*sizeof(uint64_t)+i*keylen,SEEK_SET);
            fread(akey,keylen,1,tkeys);
            fseek(tvals,2*sizeof(uint64_t)+i*vallen,SEEK_SET);
            fread(aval,vallen,1,tvals);
        }
        else
        {
            fwrite(bkey,keylen,1,okeys);
            fwrite(bval,vallen,1,ovals);
            j++;
            if(j==snd+sndlen)
                break;
            fseek(tkeys,2*sizeof(uint64_t)+j*keylen,SEEK_SET);
            fread(bkey,keylen,1,tkeys);
            fseek(tvals,2*sizeof(uint64_t)+j*vallen,SEEK_SET);
            fread(bval,vallen,1,tvals);
        }
    }
    if(i<fst+fstlen)
        for(;;)
        {
            fwrite(akey,keylen,1,okeys);
            fwrite(aval,vallen,1,ovals);
            i++;
            if(i==fst+fstlen)
                break;
            fseek(tkeys,2*sizeof(uint64_t)+i*keylen,SEEK_SET);
            fread(akey,keylen,1,tkeys);
            fseek(tvals,2*sizeof(uint64_t)+i*vallen,SEEK_SET);
            fread(aval,vallen,1,tvals);
        }
    if(j<snd+sndlen)
        for(;;)
        {
            fwrite(bkey,keylen,1,okeys);
            fwrite(bval,vallen,1,ovals);
            j++;
            if(j==snd+sndlen)
                break;
            fseek(tkeys,2*sizeof(uint64_t)+j*keylen,SEEK_SET);
            fread(bkey,keylen,1,tkeys);
            fseek(tvals,2*sizeof(uint64_t)+j*vallen,SEEK_SET);
            fread(bval,vallen,1,tvals);
        }
    delete akey;
    delete aval;
    delete bkey;
    delete bval;

}

void copytotemp(uint64_t f,uint64_t n,uint64_t keylen,uint64_t vallen)
{
    uint8_t *key=new uint8_t[keylen];
    uint8_t *val=new uint8_t[vallen];
    fseek(tkeys,2*sizeof(uint64_t)+f*keylen,SEEK_SET);
    fseek(tvals,2*sizeof(uint64_t)+f*vallen,SEEK_SET);
    fseek(okeys,2*sizeof(uint64_t)+f*keylen,SEEK_SET);
    fseek(ovals,2*sizeof(uint64_t)+f*vallen,SEEK_SET);
    for(uint64_t i=f;i<f+n;i++)
    {
        fread(key,keylen,1,okeys);
        fread(val,vallen,1,ovals);
        fwrite(key,keylen,1,tkeys);
        fwrite(val,vallen,1,tvals);
    }
    delete key;
    delete val;
}

void MergeSort2(uint64_t left, uint64_t right, uint64_t nmem, uint64_t keylen, uint64_t vallen) {
    uint64_t m,k;

    if(right-left+1<=nmem) return;
    k = (right - left + 1)/nmem;
    k=k/2+k%2;
    m = left + k*nmem;
    //cout<<"left="<<left<<" medium="<<m<<" right="<<right<<endl;
    MergeSort2(left, m-1,nmem,keylen,vallen);
    MergeSort2(m, right,nmem,keylen,vallen);
    mergefile(left,m,m-left,right-m+1,nmem,keylen, vallen);
    copytotemp(left,right-left+1,keylen,vallen);
}

void MergeSort(uint8_t *keys,uint8_t *vals, uint64_t l, uint64_t r, uint64_t keylen,uint64_t vallen )
{
    uint64_t m;

    if(l >= r) return;

    m = (l + r) / 2;

    MergeSort(keys,vals, l, m,keylen,vallen);
    MergeSort(keys,vals, m + 1, r,keylen,vallen);
    Merge(keys,vals, l, r, m,keylen,vallen);
}

void show(FILE *kk,FILE *vv,uint64_t f,uint64_t n, uint64_t keylen,uint64_t vallen)//исполюзуется, чтобы вывести в текстовй файл результат
{

    fseek(kk,2*sizeof(uint64_t)*keylen*f,SEEK_SET);
    fseek(vv,2*sizeof(uint64_t)+vallen*f,SEEK_SET);

    uint8_t *key=new uint8_t[keylen];
    uint8_t *val=new uint8_t[vallen];

    for(uint64_t i=f;i<f+n;i++) {
    fread(key,keylen,1,kk);
    fread(val,vallen,1,vv);
        for(int j=0;j<keylen;j++)
            cout << (char)key[j];
        cout << " ";
        for(int j=0;j<vallen;j++)
                cout << (char)val[j];
        cout << endl;
    }
    cout << "--------------------------------------" << endl;

    delete key;
    delete val;

}


void threadFunction(uint64_t n,uint64_t first,uint64_t keylen,uint64_t vallen)
{
    uint64_t nmem=MAXMEM/NUMTHREADS/(keylen+vallen);
    nmem=nmem<=n?nmem:n;
    uint8_t *keys=new uint8_t[keylen*nmem];
    uint8_t *vals=new uint8_t[vallen*nmem];
    uint64_t ost=n;
    uint64_t portion;
    uint64_t t,r;

    ikeys=fopen(inkeysname,"rb");
    ivals=fopen(invalsname,"rb");
    okeys=fopen(outkeysname,"r+b");
    ovals=fopen(outvalsname,"r+b");
    tkeys=fopen("tmpk","r+b");
    tvals=fopen("tmpv","r+b");

    uint64_t tmp1;
    uint64_t tmp2;

    for(portion=first;ost!=0;portion+=nmem)
    {
        t=ost>nmem?nmem:ost;
        fseek(ikeys,2*sizeof(uint64_t)+portion*keylen,SEEK_SET);
        fread(keys,keylen,t,ikeys);
        fseek(ivals,2*sizeof(uint64_t)+portion*vallen,SEEK_SET);
        fread(vals,vallen,t,ivals);

        MergeSort(keys,vals,0,t-1,keylen,vallen);

        fseek(okeys,2*sizeof(uint64_t)+portion*keylen,SEEK_SET);
        fwrite(keys,keylen,t,okeys);
        fseek(ovals,2*sizeof(uint64_t)+portion*vallen,SEEK_SET);
        fwrite(vals,vallen,t,ovals);
        copytotemp(portion,t,keylen,vallen);
        r = nmem==ost? 0:ost;
        ost-=t;
    }
    r = (t==nmem? 0:nmem-t);

    MergeSort2(first, portion-r-1,nmem,keylen, vallen);
    fclose(ikeys);
    fclose(okeys);
    fclose(tkeys);
    fclose(ivals);
    fclose(ovals);
    fclose(tvals);
    delete keys;
    delete vals;
}

bool empty(int *mass, int size)
{
    for (int i = 0; i<size; i++)
        if (mass[i] == 1)
	    return false;
    return true;
}

void insertSort(uint8_t **keys, int *idx, int size) {
    int tmpidx;

    for (int i = 1; i<size; i++) {
        int j = i-1;
        while (j>=0 && memcmp(keys[idx[j]],keys[idx[j+1]],keylen)>0) {
            tmpidx = idx[j];
            idx[j] = idx[j+1];
            idx[j+1] = tmpidx;
            j--;
        }
    }
}

void finalMerge() {
    int *ost = new int[NUMTHREADS];
    for (int i = 0; i<NUMTHREADS; i++)
        ost[i] = 1;

    uint64_t *progress = new uint64_t[NUMTHREADS];
    uint64_t *lstPositions = new uint64_t[NUMTHREADS];
    uint64_t beg = 0;
    progress[0] = beg;
    
    uint8_t  **keys = new uint8_t*[NUMTHREADS];
    for (int i = 0; i<NUMTHREADS; i++)
        keys[i] = new uint8_t[keylen];
    uint8_t **vals = new uint8_t*[NUMTHREADS];
    for (int i = 0; i<NUMTHREADS; i++)
        vals[i] = new uint8_t[vallen];
    int *idx = new int[NUMTHREADS];
    for (int i = 0; i<NUMTHREADS; i++)
        idx[i] = i;
    for(int i = 0; i<NUMTHREADS; i++) {
        if (i == 0) {
            progress[i] = beg;
            fseek(tkeys, 2*sizeof(uint64_t) + progress[i]*keylen, SEEK_SET);
            fread(keys[i],keylen,1,tkeys);
            fseek(tvals, 2*sizeof(uint64_t) + progress[i]*vallen, SEEK_SET);
            fread(vals[i],vallen,1,tvals);
            beg+=nn+n1%NUMTHREADS;
        }    
	else {
            lstPositions[i-1] = progress[i] = beg;
            fseek(tkeys, 2*sizeof(uint64_t) + progress[i]*keylen, SEEK_SET);
            fread(keys[i],keylen,1,tkeys);
            fseek(tvals, 2*sizeof(uint64_t) + progress[i]*vallen, SEEK_SET);
            fread(vals[i],vallen,1,tvals);
	    beg+=nn;
	}
    }
    lstPositions[NUMTHREADS-1] = lstPositions[NUMTHREADS - 2] + nn;
    int *howMuchToAdd = new int[NUMTHREADS];
    for (int i = 0; i<NUMTHREADS; i++)
        howMuchToAdd[i]=0;
    fseek(okeys, 2*sizeof(uint64_t), SEEK_SET);
    fseek(ovals, 2*sizeof(uint64_t), SEEK_SET);
    int num = 0;
    int numbers = NUMTHREADS;

    while(numbers>0) {

        insertSort(keys,idx, numbers);
        num=idx[0];

        fwrite(keys[num],keylen,1,okeys);
        fwrite(vals[num],vallen,1,ovals);
        progress[num]++;

            if (progress[num] == lstPositions[num]) {


                for (int l = 0; l<numbers; l++) {
                    idx[l] = idx[l+1];
                }
                numbers--;

            }
            else {
                fseek(tkeys, 2*sizeof(uint64_t) + progress[num]*keylen, SEEK_SET);
                fread(keys[num], keylen,1,tkeys);
                fseek(tvals, 2*sizeof(uint64_t) + progress[num]*vallen, SEEK_SET);
                fread(vals[num], vallen,1,tvals);
            }

    }
}

int main(int argc, char *argv[])
{

    NUMTHREADS =  thread::hardware_concurrency()>0? thread::hardware_concurrency():1;
    thread **ths=new thread*[NUMTHREADS];
    if(argc!=9)
    {
        cout << "Command: parmerge --keys <keys file> --values <values file> --out-keys <keys output file> --out-values <values output file>" << endl;
        return 1;
    }
    for(int i=1;i<argc;)
    {
        if(strcmp(argv[i],"--keys")==0)
        {
            inkeysname=argv[i+1];
            i+=2;
        }
        if(strcmp(argv[i],"--values")==0)
        {
            invalsname=argv[i+1];
            i+=2;
        }
        if(strcmp(argv[i],"--out-keys")==0)
        {
            outkeysname=argv[i+1];
            i+=2;
        }
        if(strcmp(argv[i],"--out-values")==0)
        {
            outvalsname=argv[i+1];
            i+=2;
        }
    }
    if(inkeysname==NULL||invalsname==NULL||outkeysname==NULL||outvalsname==NULL)
    {
        cout << "Command: parmerge --keys <keys file> --values <values file> --out-keys <keys output file> --out-values <values output file>" << endl;
        return 1;
    }
    ikeys=fopen(inkeysname,"rb");
    if(ikeys==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }
    ivals=fopen(invalsname,"rb");
    if(ivals==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }
    okeys=fopen(outkeysname,"w+b");
    if(okeys==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }
    ovals=fopen(outvalsname,"w+b");
    if(ovals==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }
    tkeys=fopen("tmpk","w+b");
    if(tkeys==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }
    tvals=fopen("tmpv","w+b");
    if(tvals==NULL)
    {
        cout << "Error opening file." << endl;
        return 1;
    }

    fread(&n1,sizeof(uint64_t),1,ikeys);
    fread(&keylen,sizeof(uint64_t),1,ikeys);

    fread(&n2,sizeof(uint64_t),1,ivals);
    fread(&vallen,sizeof(uint64_t),1,ivals);
    if(n1!=n2)
    {
        cout << "Error." << endl;
        return 1;
    }
    fwrite(&n1,sizeof(uint64_t),1,okeys);
    fwrite(&n1,sizeof(uint64_t),1,tkeys);
    fwrite(&keylen,sizeof(uint64_t),1,okeys);
    fwrite(&keylen,sizeof(uint64_t),1,tkeys);
    uint64_t tmp1,tmp2;

    fwrite(&n1,sizeof(uint64_t),1,ovals);
    fwrite(&n1,sizeof(uint64_t),1,tvals);
    fwrite(&vallen,sizeof(uint64_t),1,ovals);
    fwrite(&vallen,sizeof(uint64_t),1,tvals);
    uint8_t *tmp=new uint8_t[keylen>vallen?keylen:vallen];
    memset(tmp,0,keylen>vallen?keylen:vallen);
    for(uint64_t i=0;i<n1;i++)
    {
        fwrite(tmp,keylen,1,tkeys);
        fwrite(tmp,vallen,1,tvals);
        fwrite(tmp,keylen,1,okeys);
        fwrite(tmp,vallen,1,ovals);
    }
    delete tmp;
    fflush(tkeys);
    fflush(tvals);
    fflush(okeys);
    fflush(ovals);

    uint64_t beg,num;
    nn=n1/NUMTHREADS;
    if(nn==0)
    {
        NUMTHREADS=n1;
        nn=1;
    }
    for(int i=0;i<NUMTHREADS;i++)
    {
        if(i==0)
        {
            beg=0;
            num=nn+n1%NUMTHREADS;
        }
        else
        {
            beg+=num;
            num=nn;
        }
        ths[i]=new thread(threadFunction,num,beg,keylen,vallen);
    }

    for(int i=0;i<NUMTHREADS;i++)
        ths[i]->join();

    finalMerge();



    show(okeys,ovals,0,n1,keylen,vallen);


    fclose(ikeys);
    fclose(okeys);
    fclose(tkeys);
    fclose(ivals);
    fclose(ovals);
    fclose(tvals);

    remove("./tmpk");
    remove("./tmpv");

    return 0;
}
