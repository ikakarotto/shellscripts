#!/usr/bin/env python2.7
# coding: utf8
'''
用于检查文件md5是否正确,类似linux下md5sum -c md5.txt的功能
'''
import sys
import os
import hashlib



md5file = 'md5.txt'

if os.path.isfile(md5file):
    pass
else:
    print('md5file not found.')
    sys.exit(1)


for line in open(md5file, 'r').readlines():
    if len(line.split()) == 2:
        filemd5 = line.split()[0]
        filename = line.split()[1]
        # print(line.strip())

        if os.path.isfile(filename):
            fb = open(filename,'rb')
            md5 = hashlib.md5(fb.read()).hexdigest()
            fb.close()

            if filemd5 == md5:
                print(filename + ': OK')
            else:
                print(filename + ': FAILED')

        else:
            print(filename + ' not found.')

    else:
        print(line.strip() + ' data error')

