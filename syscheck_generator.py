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
file_syscheck = "/var/log/syscheck.log"
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

if os.path.isfile(file_syscheck):
    if days>0:
        print(f"WARNING! File ${file} already exists and you set day value. \n\
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
    open(file_syscheck, 'a').close()

try:
    logging.basicConfig(format='%(message)s', filename=file_syscheck, level=logging.DEBUG, encoding='utf-8')
except FileNotFoundError as err:
    print(f"{err}\n{type(err)}", file=sys.stderr)
    exit(4)

#print("2022-04-01 00:41:48 host6 Hostd: warning hostd[526387] [Originator@6876 sub=Default opID=esxui-9558-3741] Rejected password for user user-user5 from 10.16.89.3")
host_list = ["host", "host-h2", "host-ho3", "host-hos4", "host-host5", "host6", "host7", "host8", "host9", "host10"]
user_list = ["user1", "user-u2", "user-us3", "user-use4","user-user5"]
ip_list = ["10.129.210.1", "10.14.34.2", "10.16.89.3", "10.14.199.4","10.145.99.5"]

if os.path.isfile(file_syscheck):
    if days>0:
        print(f"WARNING! File ${file_syscheck} already exists and you set day value. \n\
Current file must be deleted before starting process. Do you agree? [y/n]")
        while True:
            val = input()
            if val == "n":
                exit()
            elif val == "y":
                os.remove(file_syscheck)
                open(currentValue, 'a').close()
                break
else:
    open(file_syscheck, 'a').close()

try:
    logging.basicConfig(format='%(message)s', filename=file_syscheck, level=logging.DEBUG, encoding='utf-8')
except FileNotFoundError as err:
    print(f"{err}\n{type(err)}", file=sys.stderr)
    exit(4)

sha256_list = ["797ea8d5eb44d2daa60b2ffb830d3e40259e4af19b881900cfb8079584249106", \
          "1df4d2577bd15b6c170f100cc9a3e8606ea6a9fa0f1f6aea858942b932603ab7", \
          "5910dd2fc0422caf1b1e34262cdf333a40d1a48522855d30b8595ba6a14d216b", \
          "733c9bc19762fa75e16f790940f7d934f8376e4693f41418b17ab77779fbf25f", \
          "40126b305ff6f53f7c719d751658b752327a1c6e98890e41e488d7a81fa0db45", \
          "02e837b66f177f4e41eb2f1c7ff6e4deb729a8473ac5c6e62629248d96f24622", \
          "1678d0b345a0fec2ab34f8e564086dda66fb5eff555816e1b5fe4de1e731cf9f", \
          "11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492f", \
          "542e47d9ff9767a5db0bb1479a55c275f5ca5b5d189498429ca8c96b6b0f4ffd", \
           "1d25770d00c7d73191daacdef43f5fbe434e5dbf0b6b41b646cfc50eb6b07750"]


for i in reversed(range(86400*days)):
    for x in range(4):
        if(random.randint(0,100)>15):
            continue
        dt = datetime.fromtimestamp(time.time()-i)
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
        ip = random.choices(ip_list, weights=(10, 20, 30, 40, 50), k=1)[0]
        host = random.choices(host_list, weights=(10, 20, 30, 40, 50, 60, 70, 80, 90, 100), k=1)[0]
        sha = random.choices(sha256_list, weights=(10, 20, 30, 40, 50, 60, 70, 80, 90, 100), k=1)[0]
        logging.debug('timestamp:{} hostname: {} ip:{} syscheck path:/home/clm/metricbeat/logs/metricbeat sha256:{}}}'. \
                      format(date, host, ip, sha))


if stop:
    exit()
while True:
    time.sleep(random.randint(100,3000)/1000)
    dt = datetime.fromtimestamp(time.time())
    date = dt.strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choices(ip_list, weights=(10, 20, 30, 40, 50), k=1)[0]
    host = random.choices(host_list, weights=(10, 20, 30, 40, 50, 60, 70, 80, 90, 100), k=1)[0]
    sha = random.choices(sha256_list, weights=(10, 20, 30, 40, 50, 60, 70, 80, 90, 100), k=1)[0]
    logging.debug('timestamp:{} hostname: {} ip:{} syscheck path:/home/clm/metricbeat/logs/metricbeat sha256:{}}}'. \
                  format(date, host, ip, sha))
