import random
import time
from datetime import datetime
import logging

logging.basicConfig(format='%(message)s', filename='/var/log/esxi.log', level=logging.DEBUG, encoding='utf-8')
print("This script generates logs in /var/log/esxi.log which imitate failed login attempts. They are in format:")
print("2022-04-01 00:41:48 host6 Hostd: warning hostd[526387] [Originator@6876 sub=Default opID=esxui-9558-3741] Rejected password for user user-user5 from 10.16.89.3")
host_list = ["host", "host-h2", "host-ho3", "host-hos4", "host-host5", "host6", "host7", "host8", "host9", "host10"]
user_list = ["user1", "user-u2", "user-us3", "user-use4","user-user5"]
ip_list = ["10.129.210.1", "10.14.34.2", "10.16.89.3", "10.14.199.4","10.145.99.5"]
while True:
    time.sleep(random.randint(100,3000)/1000)
    dt = datetime.fromtimestamp(time.time())
    date = dt.strftime("%Y-%m-%d %H:%M:%S")
    hostd = random.randint(525000,528000)
    hex1 = str(hex(random.randint(256,256*256-1)))[2:]
    hex2 = str(hex(random.randint(256,256*256-1)))[2:]
    user = random.choices(user_list, weights=(10,20,30,40,50), k=1)[0]
    ip = random.choices(ip_list, weights=(10,20,30,40,50), k=1)[0]
    host = random.choices(host_list, weights=(10,20,30,40,50,60,70,80,90,100), k=1)[0]
    logging.debug('{} {} Hostd: warning hostd[{}] [Originator@6876 sub=Default opID=esxui-{}-{}] Rejected password for user {} from {}'.format(date,host, hostd, hex1, hex2, user, ip))
