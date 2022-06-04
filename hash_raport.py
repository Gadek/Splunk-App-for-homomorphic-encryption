import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv
import os
from time import sleep



malicious_hashes = list()
with open("malicious hashes.txt") as f:
    for line in f:
        malicious_hashes.append(line[:-1])

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

search='search index=hashes'
create_dict = dict()
create_dict['rf'] = "hash"
create_dict['earliest_time'] = "-1h"
results_dict = dict()
# results_dict['count'] = 2
results_dict['output_mode'] = "json"
results_dict['field_list'] = "_raw hash"

def run_job(service):
    job = service.jobs.create(search,**create_dict)

    while True:
        while not job.is_ready():
            pass
        if job['isDone'] == '1':
            break
        sleep(2)

    rr1 = job.results(**results_dict)
    # print(rr1)
    search_result = results.JSONResultsReader(rr1)
    job.cancel()

    index = service.indexes["result_hashes"]
    for result in search_result:
        print(result['hash'])
        if result['hash'] in malicious_hashes:
            lastevent = "hash: {} is malicious?: True".format(result['hash'])
        else:
            lastevent = "hash: {} is malicious?: False".format(result['hash'])

        index.submit(lastevent + "\n", sourcetype="hash-check")



def main():
    load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    username = os.getenv('username')
    password = os.getenv('password')

    service = client.connect(host=host, port=port, username=username, password=password)
    assert isinstance(service, client.Service)

    run_job(service)


if __name__ == "__main__":
    main()