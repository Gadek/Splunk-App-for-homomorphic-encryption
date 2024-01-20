#import splunklib.client as client
#import splunklib.results as results
#from dotenv import load_dotenv
import os
from time import sleep,time
import splunk.Intersplunk
import sys
import subprocess

# outputs = []

# malicious_hashes = list()
# with open("malicious hashes.txt") as f:
#     for line in f:
#         malicious_hashes.append(line[:-1])

#print(malicious_hashes)

FLAGS_CREATE = [
    "earliest_time", "latest_time", "now", "time_format",
    "exec_mode", "search_mode", "rt_blocking", "rt_queue_size",
    "rt_maxblocksecs", "rt_indexfilter", "id", "status_buckets",
    "max_count", "max_time", "timeout", "auto_finalize_ec", "enable_lookups",
    "reload_macros", "reduce_freq", "spawn_process", "required_field_list",
    "rf", "auto_cancel", "auto_pause",
]

FLAGS_RESULTS = [
    "offset", "count", "search", "field_list", "f", "output_mode"
]



# def run_job(service, idx, earliest_time, latest_time):
#
#     search = 'search index='+idx
#     create_dict = dict()
#     create_dict['rf'] = "hash"
#     create_dict['earliest_time'] = earliest_time
#     create_dict['latest_time'] = latest_time
#     results_dict = dict()
#     # results_dict['count'] = 2
#     results_dict['output_mode'] = "json"
#     results_dict['field_list'] = "_raw hash"
#
#     job = service.jobs.create(search,**create_dict)
#
#     while True:
#         while not job.is_ready():
#             pass
#         if job['isDone'] == '1':
#             break
#         sleep(2)
#
#     rr1 = job.results(**results_dict)
#     # print(rr1)
#     search_result = results.JSONResultsReader(rr1)
#     job.cancel()
#
#     index = service.indexes["result_hashes"]
#     for result in search_result:
#         #print(result['hash'])
#         if result['hash'] in malicious_hashes:
#             lastevent = "{"+'"hash":"{}", "is_malicious":"True"'.format(result['hash'])+"}"
#         else:
#             lastevent = "{"+'"hash":"{}", "is_malicious":"False"'.format(result['hash'])+"}"
#
#         index.submit(lastevent + "\n", sourcetype="_json")





def main():

    if len(sys.argv) != 6:
        print("ERROR")
        print("Wrong number of arguments.")
        exit()
    if sys.argv[3] >= sys.argv[4]:
        print("ERROR")
        print("time error")
        exit()

    sourceIndex = sys.argv[1]
    option = sys.argv[2]
    time1 = sys.argv[3]
    time2 = sys.argv[4]
    analyse_bool = int(sys.argv[5])

    if analyse_bool:

        p2 = subprocess.run(
            ["/usr/bin/python3", "report.py", option,time1,time2,sourceIndex],
            capture_output=False
        )

    else:
        print("_raw")
        print("Jeśli chcesz przeanalizować dane zaznacz checkbox \"analyse\"")


if __name__ == "__main__":
    main()
