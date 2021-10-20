# -*- coding: utf-8 -*-
#处理端口扫描结果
list2=[]
with open('txtFiles/ssh_result1.txt', 'r') as f:
    for line in f.readlines():
        list1 = line.strip().split(',')
        list2.append(list1[1].strip('"'))


with open('txtFiles/ssh_result2.txt', 'w') as f:
    for i in list2:
        f.write(i + "\n")