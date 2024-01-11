#!/usr/bin/env python3
# coding: utf-8
from sys import argv
import socket
import struct

def iptoint1(ip_str):
    ip_str_to_int = lambda x: sum([256**j*int(i) for j,i in enumerate(x.split('.'))])
    ip_int = ip_str_to_int(ip_str)
    return ip_int

def iptoint2(ip_str):
    i = 0
    ip_int = 0
    for ip_part in ip_str.split('.'):
            ip_int = ip_int + int(ip_part) * 256**i
            i += 1
    return ip_int

def iptoint3(ip_str):
    ip_str_reverse = '.'.join(list(reversed(ip_str.split('.'))))
    ip_int = socket.ntohl(struct.unpack("I",socket.inet_aton(ip_str_reverse))[0])
    return ip_int

def inttoip1(ip_int):
    #ip_int_to_str = lambda x: '.'.join([str(int(x/(256**i) % 256)) for i in list(range(3,-1,-1))][::-1])
    ip_int_to_str = lambda x: '.'.join([str(int(x/(256**i) % 256)) for i in list(range(4))])
    ip_str = ip_int_to_str(ip_int)
    return ip_str

def inttoip2(ip_int):
    # 需要将负数的int类型转换为long类型，否则会socket.htonl报错OverflowError: can't convert negative value to unsigned int
    ip_str = '.'.join(list(reversed(socket.inet_ntoa(struct.pack("i", socket.htonl(ip_int & 0xffffffff ))).split('.'))))
    return ip_str

def inttoip3(ip_int):
    s = []
    for i in range(4):
        ip_part = str(int(ip_int/(256**i) % 256))
        s.append(ip_part)
    ip_str = '.'.join(s)
    return ip_str

def sign32neg(value):
    if 0x80000000 <= value <= 0xFFFFFFFF:
        value &= 0x7FFFFFFF
        value = int(value)
        value = ~value
        value ^= 0x7FFFFFFF
    return value

def ip_reverse(ipaddr):
    return '.'.join(list(reversed(ipaddr.split('.'))))


if __name__ == '__main__':
    if '.' in argv[1]:
        ip_str = argv[1]
        print(sign32neg(iptoint1(ip_str)))
        #print(sign32neg(iptoint2(ip_str)))
        #print(sign32neg(iptoint3(ip_str)))
        #if len(argv) > 2: print((sign32neg(iptoint1('.'.join(list(reversed(ip_str.split('.'))))))))
    else:
        ip_int = int(argv[1])
        print(inttoip1(ip_int))
        #print(inttoip2(ip_int))
        #print(inttoip3(ip_int))
        if len(argv) > 2: print(ip_reverse(inttoip1(ip_int)))

