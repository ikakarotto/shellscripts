#!/usr/bin/env python3
# coding: utf-8
'''
用途: 用于检查文件md5是否正确,类似linux下md5sum -c md5.txt的功能
修改时间: 2022-09-15
出处: dehai
'''
import sys
import os
import glob
import getopt
import hashlib
import time

def string_to_md5(s):
    return hashlib.md5(bytes(str(s), encoding='utf8')).hexdigest()

def file_to_md5(filename):
    if os.path.isfile(filename):
        fb = open(filename,'rb')
        md5 = hashlib.md5(fb.read()).hexdigest()
        fb.close()
        print(md5 + ' ' + filename)

def get_md5(filelists):
    for fpath in filelists:
        filecount = len(list(glob.iglob(fpath)))
        if filecount == 0:
            print('%s [Error] No such file: %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), fpath))
        elif filecount > 0:
            for filename in list(glob.iglob(fpath)):
                file_to_md5(filename)

def check_md5(md5file):
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

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:", ["help", "check="])
        #print(opts)
        #print(args)

    except getopt.GetoptError:
        print(sys.argv[0] + ' -c/--check <md5_filename>')
        sys.exit(2)

    if len(args) == 0:
        for opt, arg in opts:
            if opt in ("-h", "--help", "help"):
                print(sys.argv[0] + ' -c/--check <md5_filename>')
                sys.exit()
            elif opt in ("-c", "--check"):
                md5file = arg
                check_md5(md5file)
    else:
        get_md5(args)
    
if __name__ == "__main__":
    main(sys.argv[1:])

