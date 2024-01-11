#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from shutil import copyfile


# C:\Windows\Web\Wallpaper\Theme1\img2.jpg
# C:\Users\%username%\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets
# C:\Users\%username%\Pictures\Assets
'''
username = os.environ['USERNAME']
pic_path = 'C:\\Users\\' + username + '\\Pictures\\Assets'
# print(pic_path)
os.chdir(pic_path)
files = os.listdir()
print(files)


for file in files:
    if file.endswith('.png') or file.endswith('.py'):
        pass
    else:
        # print(file)
        try:
            os.rename(file, file + '.png')
        except Exception as e:
            print(e)
            print('[ERROR] rename ' + file + ' fail.')
        else:
            print('[INFO] rename ' + file + ' success.')


src_file = r'C:\Windows\Web\Wallpaper\Theme1\img2.jpg'
dest_file = pic_path + '\\img2020.jpg'
copyfile(src_file, dest_file)
'''


username = os.environ['USERNAME']
pic_path = 'C:\\Users\\' + username + '\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'
os.chdir(pic_path)
files = os.listdir()
print(files)


dest_path = 'C:\\Users\\' + username + '\\Pictures\\Assets'
for src_file in files:
    if src_file.endswith('.png') or src_file.endswith('.jpg'):
        copyfile(src_file, dest_path)
    else:
        copyfile(src_file, dest_path + '\\' + src_file + '.png')