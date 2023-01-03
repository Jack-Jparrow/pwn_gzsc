#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
/*
int mprotect(const void *start, size_t len, int prot);
第一个参数：开始地址（该地址应是0x1000的倍数，以页方式对齐）
第二个参数：指定长度（长度也应该是0x1000的倍数）
第三个参数：指定属性
	PROT_NONE:The memory cannot be accessed at all.完全无法访问内存。
	PROT_READ:The memory can be read.可以读取内存。
	PROT_WRITE:The memory can be modified.内存可以修改。
	PROT_EXEC:The memory can be executed.内存可以执行。
    可读可写可执行（0x111=7）W
	oj->level5
*/

int dofunc(){
	char b[0x100];
	int pagesize = getpagesize();
	//printf("%d\n",pagesize);
	//printf("%d\n",&b);
	long long int addr = (long long int)&b;
	addr = (addr >>12)<<12;
	mprotect(addr, pagesize, 7);	
	puts("input:");	
	read(0,b,0x100);
	((void (*) (void)) b)();
    return 0;
}

int main(){
    dofunc();
    return 0;
}
//gcc question_6_2.c  -fno-stack-protector -no-pie  -o question_6_2_x64
