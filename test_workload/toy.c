#include <stdio.h>

#define cache_size
#define block_size 128
#define assoc 8
#define line cache_size / block_size / assoc

chat data[block_size][line][assoc + 1];

int main()
{
  //L2 trashing
  int temp;
  int iter_max = 1000;
  for (j = 0; j < iter_max; j++)
    for (int i = 0; i < assoc + 1; ++i)
      temp += data[0][0][i];

  //I Cache trashing

}
