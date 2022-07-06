import threading
import paramiko



def req():
    while True:
        try:
            line=list.pop()#移除列表中的一个元素，并返回该元素的值
            #print(line)
            ip = line.strip().split(',')[1].strip('"')

            uname = line.strip().split(',')[4].strip('"')
            pwd = line.strip().split(',')[5].strip('"')
            #print(ip,uname,pwd)
            print("当前线程名：",threading.current_thread().name)
        except IndexError:
            break
        try:
            # 实例化ssh客户端
            ssh = paramiko.SSHClient()
            # 创建默认的白名单
            policy = paramiko.AutoAddPolicy()
            # 设置白名单
            ssh.set_missing_host_key_policy(policy)

            # 链接服务器
            #flag = flag + 1
            #print(flag)
            ssh.connect(
                hostname=ip,  # 服务器的ip

                port=22,  # 服务器的端口
                username=uname,  # 服务器的用户名
                password=pwd,  # 用户名对应的密码
                timeout=15
            )
            #print(line.strip().split(',')[1])
            # 远程执行命令
            stdin, stdout, stderr = ssh.exec_command("lscpu", timeout=15)
            # exec_command 返回的对象都是类文件对象
            # stdin 标准输入 用于向远程服务器提交参数，通常用write方法提交
            # stdout 标准输出 服务器执行命令成功，返回的结果  通常用read方法查看
            # stderr 标准错误 服务器执行命令错误返回的错误值  通常也用read方法
            # 查看结果，注意在Python3 字符串分为了：字符串和字节两种格式，文件返回的是字节
            result = stdout.read().decode()

            print(result)
            #list2.append(list[1].strip('"') + ',' + list[4].strip('"') + ',' + list[5].strip('"'))
            ssh.close()
        except Exception as e:
            print(e)
            pass




def main():
    thread_list = []
    for i in range(3):#开启三个线程

        t=threading.Thread(target=req)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()


    for t in thread_list:
        t.join()

if __name__ == '__main__':
    list=[]

    with open('txtFiles/ssh_result1.txt', 'r') as f:
        for element in f.readlines():
            element2 = element.strip()
            url = element2
            list.append(url)
    main()