#把零碎的IP段整合到一起（第二版）
with open('txtFiles/1.txt', 'r') as f:
    for line in f.readlines():
        list1 = line.strip().split('\t')
        list2 = list1[0].split('.')
        list3 = list1[1].split('.')


        if (list2[0] == list3[0]):  # 所有IP在同一个A段
            if (list2[1] == list3[1]):  # 所有IP在同一个B段

                list4 = []
                for i in range(int(list2[2]), int(list3[2]) + 1):
                    for j in range(256):
                        start = list2[0] + '.' + list2[1]
                        start = start + '.' + str(i)
                        start = start + '.' + str(j)
                        # print(start)
                        list4.append(start)

                with open('txtFiles/ipList.txt', 'a') as f:
                    for i in list4:
                        f.write(i + "\n")
            else:  # IP处在同一个A段，但是不同B段
                list5 = []
                #print(list2[1])
                #print(list3[1])

                #先处理第一个B段，防止碰到第一个B段不是满段的情况
                for i in range(int(list2[2]),256):
                    for j in range(256):
                        start = list2[0] + '.' + list2[1]
                        start = start + '.' + str(i)
                        start = start + '.' + str(j)
                        list5.append(start)

                for i in range(int(list2[1])+1, int(list3[1])):#再处理中间几个B段
                    for j in range(256):
                        for k in range(256):
                            start = list2[0]
                            start = start + '.' + str(i)
                            start = start + '.' + str(j)
                            start = start + '.' + str(k)
                            # print(start)
                            list5.append(start)

                for i in range(0,int(list3[2]) + 1):#再处理最后一个B段，防止碰到最后一个B段不是满段的情况
                    for j in range(256):
                        start = list3[0] + '.' + list3[1]
                        start = start + '.' + str(i)
                        start = start + '.' + str(j)
                        list5.append(start)


                with open('txtFiles/ipList.txt', 'a') as f:
                    for i in list5:
                        f.write(i + "\n")
        else:
            print(list1)

    # print(line.strip().split('\t'))