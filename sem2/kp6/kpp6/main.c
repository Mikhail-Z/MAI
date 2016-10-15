#include <stdio.h>
#include "point.h"
#include "functions.h"

void usage()
{
  printf("Usage: program filename -p \n");
}

int main(int argc, char* argv[])
{
  int flag_p=0;
  char* binfilename;
  if (argc < 2) {
    usage();
    return 1;
  }
  else {
     binfilename = argv[1];
     int i;
     for (i = 2; i < argc; i++) {
         if (strcmp(argv[i],"-p+") == 0) flag_p=2;
         if (strcmp(argv[i],"-p-") == 0) flag_p=1;
     }
  }
  country c;

  FILE *in = fopen(binfilename, "rb");
  if (!in) {
    perror("Can't open file");
    return 2;
  }
  double space_sum = 0;
  int population_sum = 0;
  int n = 0;
  while (fread(&c, sizeof(c), 1, in) == 1) {
    n++;
    space_sum += c.space;
    population_sum+=c.population;
  }
  fseek(in, 0, SEEK_SET);
  if (n == 0) {
    printf("No countries, average age is not defined\n");
    return 3;
  }
  double sr;
  if (space_sum != 0) {sr = population_sum/space_sum;}
  else printf (" total space = 0, something wrong");
  while (fread(&c, sizeof(c), 1, in) == 1)
    if (flag_p == 0 || flag_p == 2) {
      if (c.population/c.space > sr)
         printf("%s %d %s %.1f\n",c.name, c.population, c.capital, c.space);
    }
    else if (flag_p == 1) {
        if (c.population/c.space < sr)
           printf("%s %d %s %lf\n",c.name, c.population, c.capital, c.space);
    }
  return 0;
}






















