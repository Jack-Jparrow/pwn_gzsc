#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int dofunc(){
	char b[0x100];
	puts("input:");	
	read(0,b,0x100);
	((void (*) (void)) b)();
    return 0;
}

int main(){
    dofunc();
    return 0;
}
