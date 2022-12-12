#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int dofunc(){
    char b[8] = {};
	write(1,"input:",6);//2,3,4 fd=open('./a');puts
	read(0,b,0x100);
	write(1,"byebye",6);
    return 0;
}

int main(){
    dofunc();
    return 0;
}
