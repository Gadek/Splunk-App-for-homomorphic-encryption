import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv
import os
import sys
from time import sleep
import pickle

from Pyfhel import Pyfhel

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

from src.operations.AddNumbersOperation import AddNumbersOperation
from src.operations.AreStringsPresentInTableOperation import AreStringsPresentInTableOperation
from src.operations.FindMaliciousHashesOperation import FindMaliciousHashesOperation

from socket_utils import process

# FLAGS_CREATE = [
#     "earliest_time", "latest_time", "now", "time_format",
#     "exec_mode", "search_mode", "rt_blocking", "rt_queue_size",
#     "rt_maxblocksecs", "rt_indexfilter", "id", "status_buckets",
#     "max_count", "max_time", "timeout", "auto_finalize_ec", "enable_lookups",
#     "reload_macros", "reduce_freq", "spawn_process", "required_field_list",
#     "rf", "auto_cancel", "auto_pause",
# ]
#
# FLAGS_RESULTS = [
#     "offset", "count", "search", "field_list", "f", "output_mode"
# ]



def __shorten_hashes(hashes):
    short_hashes = []

    for h in hashes:
        short_hashes += [
            h[:]
        ]

    return short_hashe

def __getHEContext():
    if os.path.exists('HE_context_and_keys'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys')
        return HE

    HE = Pyfhel()
    HE.contextGen(scheme='bfv', n=2**15, t_bits=34)
    HE.keyGen()

    PyfhelUtils.saveHE('HE_context_and_keys', HE)

    return HE

def run_job(service, idx, earliest_time, latest_time):
    search = 'search index=' + idx + ' | head 5'
    create_dict = dict()
    create_dict['rf'] = "hash"
    create_dict['earliest_time'] = earliest_time
    create_dict['latest_time'] = latest_time
    results_dict = dict()
    results_dict['count'] = 0
    results_dict['output_mode'] = "json"
    results_dict['field_list'] = "_raw hash"
    search_result = get_hashes(service, search, create_dict, results_dict)

    HE = __getHEContext()

    operation = prepare_operation(HE, search_result)
    received = process(pickle.dumps(operation))      # send prepared operation to processor
    res = pickle.loads(received)

    # ######### replaced with sockets #############
    # FileIO.savePickle('fileA.pickle', operation)
    # print("Please run processor with input file=fileA.pickle and output file=fileB.pickle")
    # print("Then press ENTER")
    # tmp = input()
    #
    # res = FileIO.loadPickle('fileB.pickle')
    # #############################################
    result_logs = decrypt_result(HE, res)

    send_result_hashes(service, result_logs)

def get_hashes(service, search, create_dict, results_dict):
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

    return search_result

def prepare_operation(HE, search_result):
    hashes_to_check = []

    for result in search_result:
        print("search res:", result)
        hashes_to_check += [
            result['hash']
        ]

    operation = FindMaliciousHashesOperation(hashes_to_check)
    operation.encrypt(HE)

    return operation

def decrypt_result(HE, res):
    res.decrypt(HE)
    return res.toLogs()

def send_result_hashes(service, result_logs):
    index = service.indexes["result_hashes"]
    i=0
    for result in result_logs:
        i += 1
        print(result)
        index.submit(result, sourcetype="hash-check")
    print(i)


def main():
    # load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    # username = os.getenv('username')
    # password = os.getenv('password')
    token = os.getenv('token')
    service = client.connect(host=host, port=port, token=token)
    assert isinstance(service, client.Service)

    idx = sys.argv[1]
    #dest_idx = sys.argv[2]
    time1 = sys.argv[3]
    time2 = sys.argv[4]
    #service = sys.argv[5]

    run_job(service, idx, time1, time2)


if __name__ == "__main__":
    main()
