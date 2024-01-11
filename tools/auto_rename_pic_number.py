#!/usr/bin/env python3
# coding: utf8
import glob
import sys
import os
import time

while True:
    # 获取当前脚本目录并切换到目录中
    # basepath = os.path.dirname(sys.argv[0])
    #basepath = os.path.split(os.path.realpath(__file__))[0]

    #os.chdir(basepath)
    #print(basepath)
    
    # 获取所有文件列表
    filelist = os.listdir('./')
    print(filelist)
    
    # 获取所有图片
    piclist = []
    for filename in filelist:
        if '.jpg' in filename or '.png' in filename:
            piclist.append(filename)
    
    # 获取已命名和未命名的文件
    numlist = []
    strlist = []
    
    for picname in piclist:
        nameprefix = picname.split('.')[0]
        try:
            numlist.append(int(nameprefix))
        except ValueError:
            strlist.append(picname)
        except Exception as err:
            print(err)
    
    # print(numlist)
    # print(strlist)
    
    # 获取最大序号的图片数字
    try:
        if numlist:
            maxnum = max(numlist)
    
            # 修改文件名
            for picsrc in strlist:
                try:
                    nextname = str(maxnum+1) + '.jpg'
                    # print(strlist[0],nextname)
                    os.rename(picsrc,nextname)
                    maxnum += 1
                except Exception as err:
                    print(err)
        
                time.sleep(0.3)
        
            time.sleep(0.5)
        else:
            print("未找到纯数字的jpg或png图片")
            print("No jpg or png images found for purely numeric filenames.")
            time.sleep(15)

            break

    except Exception as e:
        raise e






