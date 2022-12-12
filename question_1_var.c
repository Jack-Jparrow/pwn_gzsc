#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char sh[]="/bin/sh";
int init_func(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
    return 0;
}

int func(char *cmd){
	system(cmd);
	return 0;
}

int main(){
    char a[23] = {};
    char b[71] = {};
    //char a[1] = {'b'};
	puts("input:");
	gets(b);  
	printf(b);
	if(a[0]==0x61){ 
		func(sh);
	}
    return 0;
}
