#include <stdio.h>

int main(){
  int i;
  int k = 3;

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

  return 0;
}
