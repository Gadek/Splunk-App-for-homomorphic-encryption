import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv
import sys
import os
from time import sleep
import json
from splunklib.binding import HTTPError

search='search index=test "rejected"'
verbose=0

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
create_dict = dict()
create_dict['earliest_time'] = "10"
results_dict = dict()
# results_dict['count'] = 2
results_dict['output_mode'] = "json"
results_dict['field_list'] = "_indextime _subsecond _raw"

def job(service):
    job = service.jobs.create(search,**create_dict)
    while True:
        while not job.is_ready():
            pass
        stats = {'isDone': job['isDone'],
                 'doneProgress': job['doneProgress'],
                 'scanCount': job['scanCount'],
                 'eventCount': job['eventCount'],
                 'resultCount': job['resultCount']}
        progress = float(stats['doneProgress']) * 100
        scanned = int(stats['scanCount'])
        matched = int(stats['eventCount'])
        results1 = int(stats['resultCount'])
        if verbose > 0:
            status = ("\r%03.1f%% | %d scanned | %d matched | %d results" % (
                progress, scanned, matched, results1))
            sys.stdout.write(status)
            sys.stdout.flush()
        if stats['isDone'] == '1':
            if verbose > 0: sys.stdout.write('\n')
            break
        sleep(2)

    if 'count' not in results_dict: results_dict['count'] = 0
    rr1 = job.results(**results_dict)
    rr = results.JSONResultsReader(rr1)

    # while True:
    #     content = results.read(1024)
    #     if len(content) == 0: break
    #     sys.stdout.write(content.decode('utf-8'))
    #     sys.stdout.flush()
    # sys.stdout.write('\n')

    job.cancel()
    lista = []
    for result in rr:
        print(result)
        #lista.append("{}{}".format(result['_indextime'],result['_subsecond']))
    #print(lista)
    #seen = set()
    #dupes = []

    # for x in lista:
    #     if x in seen:
    #         dupes.append(x)
    #     else:
    #         seen.add(x)
    # print(dupes)
def main():
    load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    username = os.getenv('username')
    password = os.getenv('password')

    service = client.connect(host=host, port=port, username=username, password=password)
    assert isinstance(service, client.Service)

    job(service)


if __name__ == "__main__":
    main()