#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char sh[]="/bin/sh";

int func(char *cmd){
	system(sh);
	return 0;
}

int dofunc(){
    char b[8] = {};
	puts("input:");
	read(0,b,0x100);
	//printf(b);
    return 0;
}

int main(){
    dofunc();
    return 0;
}
