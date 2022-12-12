#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char sh[]="/bbbbbbbbbbbbbbbbbbin/sh";

int func(char *cmd){
	system(cmd);
	return 0;
}

int dofunc(){
    char b[8] = {};
	puts("input:");
	read(0,b,0x1c);
    return 0;
}

int main(){
    dofunc();
    return 0;
}
