# -*- coding: utf-8 -*-
list2=[]
with open('txtFiles/portscan.log', 'r') as f:
    for line in f.readlines():
        list1 = line.strip().split(':')
        list2.append(list1[0])

with open('txtFiles/portscan_new.txt', 'a') as f:
    for i in list2:
        f.write(i + "\n")