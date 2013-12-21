#include "ptlcalls.h"
#include <stdio.h>

int main(){
  int i;
  int k = 3;

  //Create checkpoint
  ptlcall_checkpoint_generic("Test_Point", PTLCALL_CHECKPOINT_AND_SHUTDOWN);

  for (i = 0; i < 1000000; i++){
    k++;
  }

  printf("%d", k);

  for (i = 0; i < 10000; i++){
    asm volatile(
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "nop;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 "addq %rbx, %rax;"
		 );
  }
  printf("TEST DONE");

  for (i = 0; i < 1000000; i++){
    k++;
  }

  printf("%d", k);

  printf("Stopping simulation\n");
  ptlcall_kill();
  return 0;
}
