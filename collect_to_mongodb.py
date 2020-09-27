# -*- coding: utf-8 -*-
#处理扫描结果中的错误和无用IP，并生成新的结果
import pymongo

list1=[]
with open('txtFiles/mongodb_result.txt','r') as f:
    for element in f.readlines():
        element2 = element.strip().split(',')[1].strip('"')
        list1.append(element2)
        #print(element2)

list2=[]
flag=0

for i in list1:
    try:
        flag=flag+1
        print(flag)
        myclient = pymongo.MongoClient('mongodb://'+i+':27017/')
        dblist = myclient.list_database_names()
        resultList = []
        for j in dblist:

            if j == 'admin':
                pass
            elif j == 'config':
                pass
            elif j == 'local':
                pass
            else:

                db = myclient[j]
                colist = db.list_collection_names(session=None)
                countList = []
                for k in colist:
                    collection=db[k]
                    count=collection.find().count()
                    countList.append(count)
                    #print(k+":"+str(count))

                for m in countList:
                    resultList.append(m>100)
        print(resultList)
        if True not in resultList:
            dblist=['READ_ME_TO_RECOVER_YOUR_DATA']

        if 'READ_ME_TO_RECOVER_YOUR_DATA' not in dblist:
            print(dblist)
            list2.append(i)
        else:
            if len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA']).union(set(dblist))))==1:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA','admin']).union(set(dblist))))==2:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'config']).union(set(dblist)))) == 2:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'local']).union(set(dblist)))) == 2:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'admin','config']).union(set(dblist)))) == 3:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'admin','local']).union(set(dblist)))) == 3:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'local', 'config']).union(set(dblist)))) == 3:
                pass

            elif len(list(set(['READ_ME_TO_RECOVER_YOUR_DATA', 'admin','config','local']).union(set(dblist)))) == 4:
                pass
            else:
                print(dblist)
                list2.append(i)
    except:
        pass
    continue

with open('txtFiles/mongodb_result2.txt', 'a') as f:
    for i in list2:
        f.write(i + "\n")

