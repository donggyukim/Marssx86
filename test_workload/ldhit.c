#include <stdio.h>

int main(){
  int i;
  asm volatile("mov (%rsp), %rax;");

  for (i = 0; i < 100000; i++){
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
		 );
  }

  asm volatile("mov (%rsp), %rax;"
	       "add %rax, %rbx");
  
  printf("TEST DONE");
  return 0;
}
