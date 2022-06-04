#testowa zmiana
import random
import time
from datetime import datetime
import logging
import getopt, sys
import os

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
# Options
options = "hsd:f:"
# Long options
long_options = ["help", "stop" "days:", "file:"]

#Default values
file = "/var/log/esxi.log"
days = 0
stop = False
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("\
This script generates logs which imitate failed login attempts to VMware ESXi. \n\n\
    Usage: python3 esxi_logs_generator.py [OPTIONS...] \n\
    General Options \n\
    -h, --help           Prints a short help text and exists\n\
    -d, --days <value>   Set number of days in past to generate logs. Default 0\n\
    -f, --file <path>    Set log file. Default /var/log/esxi.log \n\
    -s, --stop           Don't generate logs continuously")
            exit()

        elif currentArgument in ("-d", "--days"):
            try:
                days = int(currentValue)
            except ValueError as err:
                print(f"{err}\n{type(err)}", file = sys.stderr)
                exit(1)
        elif currentArgument in ("-f", "--file"):
            try:
                file = currentValue
            except ValueError as err:
                print(f"{err}\n{type(err)}", file = sys.stderr)
                exit(2)
        elif currentArgument in ("-s", "--stop"):
            stop = True

except getopt.error as err:
    # output error, and return with an error code
    print(str(err), file = sys.stderr)
    exit(3)

if os.path.isfile(file):
    if days>0:
        print("WARNING! File already exists and you set day value. \n\
Current file must be deleted before starting process. Do you agree? [y/n]")
        while True:
            val = input()
            if val == "n":
                exit()
            elif val == "y":
                os.remove(file)
                open(currentValue, 'a').close()
                break
else:
    open(file, 'a').close()

try:
    logging.basicConfig(format='%(message)s', filename=file, level=logging.DEBUG, encoding='utf-8')
except FileNotFoundError as err:
    print(f"{err}\n{type(err)}", file=sys.stderr)
    exit(4)

#print("2022-04-01 00:41:48 host6 Hostd: warning hostd[526387] [Originator@6876 sub=Default opID=esxui-9558-3741] Rejected password for user user-user5 from 10.16.89.3")
host_list = ["host", "host-h2", "host-ho3", "host-hos4", "host-host5", "host6", "host7", "host8", "host9", "host10"]
user_list = ["user1", "user-u2", "user-us3", "user-use4","user-user5"]
ip_list = ["10.129.210.1", "10.14.34.2", "10.16.89.3", "10.14.199.4","10.145.99.5"]


for i in reversed(range(86400*days)):
    for x in range(4):
        if(random.randint(0,100)>15):
            continue
        dt = datetime.fromtimestamp(time.time()-i)
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
        hostd = random.randint(525000, 528000)
        hex1 = str(hex(random.randint(256, 256 * 256 - 1)))[2:]
        hex2 = str(hex(random.randint(256, 256 * 256 - 1)))[2:]
        user = random.choices(user_list, weights=(10, 20, 30, 40, 50), k=1)[0]
        ip = random.choices(ip_list, weights=(10, 20, 30, 40, 50), k=1)[0]
        host = random.choices(host_list, weights=(10, 20, 30, 40, 50, 60, 70, 80, 90, 100), k=1)[0]
        logging.debug(
            '{} {} Hostd: warning hostd[{}] [Originator@6876 sub=Default opID=esxui-{}-{}] Rejected password for user {} from {}'.format(
                date, host, hostd, hex1, hex2, user, ip))

if stop:
    exit()
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
