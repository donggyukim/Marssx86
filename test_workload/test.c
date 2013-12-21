#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <sys/mman.h>
#include "ptlcalls.h"


//I-Cache parameter
#define icache_size 4096
#define iassoc 1
#define icache_set_size (icache_size / iassoc)

//D-Cache parameter
#define dcache_size (1024 * 1024)
#define dassoc 8
#define dcache_set_size (dcache_size / dassoc)

char data[dassoc + 1][dcache_set_size];


//input character array should have enought space to holding cache size + a set of cache
//code buffer should be aligned by page size
void icache_thrashing_gen(char *code_buffer, int iter){
  char nop = '\x90';
  char *cmp_eax_0 = "\x83\xf8";
  char *sub_eax_1 = "\x83\xe8\x01";
  char *jne = "\x0f\x85";
  char jmp = '\xe9';
  char ret = '\xc3';
  char push_rax = '\x50';
  char pop_rax = '\x58';
  int i = 0;
  int addr = icache_set_size - 5;
  char mov_num_eax = '\xb8';
  //Set iteration number
  code_buffer[i++] = push_rax;
  code_buffer[i++] = mov_num_eax;
  strncpy(code_buffer + i, (char *)&iter, 4);
  i += 4;
  code_buffer = code_buffer + i;
  i = 0;
  while(i <= icache_size){
    if (!(i % icache_set_size)){
      if (i != icache_size){
	//jmp code
	code_buffer[i++] = jmp;
	//insert address;
	strncpy(code_buffer + i, (char *)&addr, 4);
	i += 4;
      }
      else{
	//check iteration couter
	strcpy(code_buffer + i, sub_eax_1);
	i += strlen(sub_eax_1);
	strcpy(code_buffer + i, cmp_eax_0);
	i += strlen(cmp_eax_0);
	code_buffer[i++] = '\x00';
	//if it is over the threshold
	//exit jmp loop
	strcpy(code_buffer + i, jne);
	i += strlen(jne);
	addr = -(i+4);
	strncpy(code_buffer + i, (char *)&addr, 4);
	i += 4;
	//Return
	code_buffer[i++] = pop_rax;
	code_buffer[i++] = ret;
      }
    } 
    else{
      //nop
      code_buffer[i++] = nop;
    }
  }
}

int main()
{
  int a, b;
  char *code_buffer;
  int code_buffer_page_num;
  int page_size = sysconf(_SC_PAGE_SIZE);
  int code_buffer_size;
  int icache_iter = 10000;
  int dcache_iter = 100000;
  int branch_iter = 100000;
  int float_iter = 10000;
  int i,j;
  int temp;
  float float_temp = 1234.1234;

  code_buffer_page_num = ((icache_size + icache_set_size) / page_size);
  code_buffer_size = (code_buffer_page_num + 1) * page_size;
  code_buffer = (char *) memalign(page_size, code_buffer_size);

  if (!mprotect(code_buffer, code_buffer_size, PROT_EXEC | PROT_READ | PROT_WRITE))
    printf("Success in disabling protection\n");

  icache_thrashing_gen(code_buffer, icache_iter);
  //Create checkpoint
  ptlcall_checkpoint_generic("CP_TEST", PTLCALL_CHECKPOINT_AND_SHUTDOWN);

  /* //I Cache thrashing */
  /* ((void (*)())code_buffer)();  */

  /* //D Cache thrashing */
  /* for (i = 0; i < dcache_iter; ++i) */
  /*   for (j = 0; j < dassoc + 1; ++j) */
  /*     temp += data[j][0]; */

  /* //Long lat */
  /* for (i = 0; i < float_iter; ++i) */
  /*   float_temp += 1234.5669; */
  
  //Branch miss prediction hazard
  j = 0;
  for (i = 0; i < branch_iter; ++i)
    if (j)
      j = 0;
    else
      j = 1;

  ptlcall_kill();

  return 0;
}
