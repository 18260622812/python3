import paramiko

list1=[]
with open('txtFiles/ssh_result2.txt','r') as f:
    for element in f.readlines():
        element2 = element.strip()
        list1.append(element2)
        #print(element2)
username_list = ['root']
pwd_list = ['root']

list2=[]
flag=0
for i in list1:
    for j in username_list:
        for k in pwd_list:
            try:
                # 实例化ssh客户端
                ssh = paramiko.SSHClient()
                # 创建默认的白名单
                policy = paramiko.AutoAddPolicy()
                # 设置白名单
                ssh.set_missing_host_key_policy(policy)
                # 链接服务器
                flag = flag + 1
                print(flag)
                ssh.connect(
                    hostname=i,  # 服务器的ip
                    port=22,  # 服务器的端口
                    username=j,  # 服务器的用户名
                    password=k, # 用户名对应的密码
                    timeout = 15
                )
                # 远程执行命令
                stdin, stdout, stderr = ssh.exec_command("ls",timeout=15)
                # exec_command 返回的对象都是类文件对象
                # stdin 标准输入 用于向远程服务器提交参数，通常用write方法提交
                # stdout 标准输出 服务器执行命令成功，返回的结果  通常用read方法查看
                # stderr 标准错误 服务器执行命令错误返回的错误值  通常也用read方法
                # 查看结果，注意在Python3 字符串分为了：字符串和字节两种格式，文件返回的是字节
                result = stdout.read().decode()
                print(result)
                list2.append(i+','+j+','+k)
                ssh.close()
            except:
                pass
            continue


with open('txtFiles/ssh_result3.txt', 'w') as f:
    for i in list2:
        f.write(i + "\n")