void usage()
{
  printf("Usage: program filename\n");
}

int append(char* filename, country s) {
    FILE *f1=fopen(filename, "ab");
    if (f1==NULL) {
        return 1; //ошибка доступа к файлу
    }
    if (!fwrite(&s, sizeof(s), 1, f1)) {
        return 2; //ошибка записи в файл
    }
    fclose(f1);
    return 0;
}

int TxtToBin(char* txtfilename, char* binfilename)
{
    FILE *in;
    country c;
    int s=sizeof(c);
    char mystring[100];
    if ((in=fopen(txtfilename, "r")) != NULL)
    {
        while (!feof(in)) {
        if (fgets(mystring, 100, in) != NULL ) {
            char* pch = strtok (mystring," ");
            int i=0;
            while (pch != "\0")
              {
                    switch(i)
                    {
                        case 0: strcpy(c.name,pch); break;
                        case 1: c.population = atoi(pch); break;
                        case 2: strcpy(c.capital,pch); break;
                        case 3: c.space = atoi(pch); break; // from *char to int
                    }
                    pch = strtok (NULL, " ");
                    i++;
              }
            append(binfilename, c);
        }
    }
        fclose(in);
    }    
    else return 1;//ошибка открытия текстового файла

    return 0;
}

int main(int argc, char* argv[])
{
  if (argc != 4) {
    usage();
    return 1;
  }
  country c;

  FILE *in = fopen("binary.dat", "rb");
  if (!in) {
    perror("Can't open file");
    return 2;
  }
  int space_sum = 0;
  int population_sum = 0;
  while (fread(&c, sizeof(c), 1, in) == 1) {
    space_sum += c.space;
    population_sum+=c.population;
  }
  fseek(in, 0, SEEK_SET);
  if (n == 0) {
    printf("No countries, average age is not defined\n");
    return 3;
  }
  double sr = population_sum/space_sum;
  while (fread(&c, sizeof(c), 1, in) == 1)
    if (c.population+c.space < sr)
      printf("%s\n", c.country);
  return 0;
}
