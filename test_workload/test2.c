#include <stdio.h>

int main()
{
  __asm__ __volatile__ ("old:;"
			"movl $10, %eax;"
			"subl $1, %eax;"
			"cmpl $0, %eax;"
			"pushq %rax;"
			"popq %rax;"
			"ret");
  
  return 0;
}
