import random
import time
from datetime import datetime
import logging
import getopt, sys
import os
import json
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
# Options
options = "hsd:f:"
# Long options
long_options = ["help", "auth", "stop" "days:", "file:"]
# Decide whether generate hashes or auth. Default are hashes
generate_hashes=True

#Default values
file_hashes = "/var/log/hashes.log"
file_auth = "/var/log/auth.log"
days = 0
stop = False
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("\
This script generates logs regarding either: hashes of various example files or authentication attempts. \n\n\
    Usage: python3 hashes_generator.py [OPTIONS...] \n\
    General Options \n\
    -h, --help           Prints a short help text and exists\n\
    --auth               Generate logs regarding authentication attempts. Default are hashes\n\
    -d, --days <value>   Set number of days in past to generate logs. Default 0\n\
    -f, --file <path>    Set log file. Default /var/log/hashes.log \n\
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
        elif currentArgument in ("--auth"):
            generate_hashes = False

except getopt.error as err:
    # output error, and return with an error code
    print(str(err), file = sys.stderr)
    exit(3)

if 'file' not in vars():
    if generate_hashes:
        file = file_hashes
    else:
        file = file_auth

if os.path.isfile(file) and days>0:

    print(f"WARNING! File {file} already exists and you set day value. \n\
Current file must be deleted before starting process.")
    while True:
        print("Do you agree? [y/n]")
        val = input()
        if val == "n":
            exit()
        elif val == "y":
            os.remove(file)
            open(file, 'a').close()
            break
else:
    open(file, 'a').close()

try:
    logging.basicConfig(format='%(message)s', filename=file, level=logging.DEBUG)
except FileNotFoundError as err:
    print(f"{err}\n{type(err)}", file=sys.stderr)
    exit(4)

host_list = list()
with open("host_list.txt") as f:
    [host_list.append(line.split()) for line in f.readlines()]

user_list = list()
with open("user_list.txt") as f:
    [user_list.append(line.split()) for line in f.readlines()]

ip_list = list()
with open("ip_list.txt") as f:
    [ip_list.append(line.split()) for line in f.readlines()]

sha256_list = list()
with open("sha256_list.txt") as f:
    [sha256_list.append((line.split()[0], line.split()[1])) for line in f.readlines()]

ip_weights = random.sample(range(10, len(ip_list)+10), len(ip_list))
user_weights = random.sample(range(10, len(user_list)+10), len(user_list))
host_weights = random.sample(range(10, len(host_list)+10), len(host_list))
sha256_weights = random.sample(range(10, len(sha256_list)+10), len(sha256_list))

if generate_hashes:
    for i in reversed(range(86400*days)):
        for x in range(4):
            if(random.randint(0,100)>15):
                continue
            dt = datetime.fromtimestamp(time.time()-i)
            date = dt.strftime("%Y-%m-%d %H:%M:%S")
            ip = random.choices(ip_list, weights=ip_weights, k=1)[0][0]
            host = random.choices(host_list, weights=host_weights, k=1)[0][0]
            sha, file = random.choices(sha256_list, weights=sha256_weights, k=1)[0]
            logging.debug("{" + '"timestamp":"{}", "host":"{}", "ip":"{}", "path":"{}", "hash":"{}"'. \
                          format(date, host, ip, file, sha) + "}")

    if stop:
        exit()
    while True:
        time.sleep(random.randint(100,3000)/1000)
        dt = datetime.fromtimestamp(time.time())
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
        ip = random.choices(ip_list, weights=ip_weights, k=1)[0][0]
        host = random.choices(host_list, weights=host_weights, k=1)[0][0]
        sha, file = random.choices(sha256_list, weights=sha256_weights, k=1)[0]
        logging.debug("{"+'"timestamp":"{}", "host":"{}", "ip":"{}", "path":"{}", "hash":"{}"'. \
                      format(date, host, ip, file, sha)+"}")

else:
    for i in reversed(range(86400 * days)):
        for x in range(4):
            if (random.randint(0, 100) > 15):
                continue
            dt = datetime.fromtimestamp(time.time() - i)
            date = dt.strftime("%Y-%m-%d %H:%M:%S")
            user = random.choices(user_list, weights=user_weights, k=1)[0]
            ip = random.choices(ip_list, weights=ip_weights, k=1)[0]
            host = random.choices(host_list, weights=host_weights, k=1)[0]
            logging.debug("{" + '"timestamp":"{}", "info":"Authentication attempt. Rejected password.", "process":"Hostd", "host":"{}", "source_ip":"{}", "user":"{}"'. \
                          format(date, host, ip, user) + "}")

    if stop:
        exit()
    while True:
        time.sleep(random.randint(100, 3000) / 1000)
        dt = datetime.fromtimestamp(time.time())
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
        user = random.choices(user_list, weights=user_weights, k=1)[0][0]
        ip = random.choices(ip_list, weights=ip_weights, k=1)[0][0]
        host = random.choices(host_list, weights=host_weights, k=1)[0][0]
        logging.debug(
            "{" + '"timestamp":"{}", "info":"Authentication attempt. Rejected password.", "process":"Hostd", "host":"{}", "source_ip":"{}", "user":"{}"'. \
            format(date, host, ip, user) + "}")

