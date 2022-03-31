import random
import time
from datetime import datetime
hosts=["host", "host-h2", "host-ho3", "host-hos4", "host-host5", "host6", "host7", "host8", "host9", "host10"]
while True:
    time.sleep(random.randint(100,2000)/1000)
    dt = datetime.fromtimestamp(time.time())
    date = dt.strftime("%Y-%m-%d %H:%M:%S")
    hostd = random.randint(525000,528000)
    hex1 = str(hex(random.randint(256,256*256-1)))[2:]
    hex2 = str(hex(random.randint(256,256*256-1)))[2:]
    user = random.choices(["user1", "user-u2", "user-us3", "user-use4","user-user5"], weights=(10,20,30,40,50), k=1)[0]
    ip = random.choices(["10.129.210.1", "10.14.34.2", "10.16.89.3", "10.14.199.4","10.145.99.5"], weights=(10,20,30,40,50), k=1)[0]
    print('{} Hostd: warning hostd[{}] [Originator@6876 sub=Default opID=esxui-{}-{}] Rejected password for user {} from {}'.format(date, hostd, hex1, hex2, user, ip))
