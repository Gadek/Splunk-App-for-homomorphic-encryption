import sys
import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv
import os
from time import sleep
import pickle

from Pyfhel import Pyfhel

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

from src.operations.FindMaliciousHashesOperation import FindMaliciousHashesOperation
from src.operations.IpGroupAndCountOperation import IpGroupAndCountOperation

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

class Report:
    def __init__(self):
        self.search=''
        self.create_dict = dict()
        self.results_dict = dict()

        self.result_index = ''
        self.sourcetype = ''
    
    def generate(self, service):
        search_result = self._perform_search(service)
        HE = self._getHEContext()
        operation = self._prepare_operation(HE, search_result)
        
        received = process(pickle.dumps(operation))      # send prepared operation to processor
        res = pickle.loads(received)

        ########## replaced with sockets #############
        # FileIO.savePickle('fileA.pickle', operation)
        # print("Please run processor with input file=fileA.pickle and output file=fileB.pickle")
        # print("Then press ENTER")
        # tmp = input()

        # res = FileIO.loadPickle('fileB.pickle')
        ##############################################

        resultLogs = self._decrypt_result(HE, res)
        self._send_result(service, resultLogs)
    
    def _perform_search(self, service):
        job = service.jobs.create(self.search, **self.create_dict)

        while True:
            while not job.is_ready():
                pass
            if job['isDone'] == '1':
                break
            sleep(2)

        rr1 = job.results(**self.results_dict)
        # print(rr1)
        search_result = results.JSONResultsReader(rr1)
        job.cancel()

        return search_result
    
    def _getHEContext(self):
        if os.path.exists('HE_context_and_keys_basic'):
            HE = PyfhelUtils.loadHE('HE_context_and_keys_basic')
            return HE

        HE = Pyfhel()
        HE.contextGen(scheme='bfv', n=2**15, t_bits=34)
        HE.keyGen()
        
        PyfhelUtils.saveHE('HE_context_and_keys_basic', HE)

        return HE
    
    def _prepare_operation(self, HE, search_result):
        raise NotImplementedError("Please Implement this method")
    
    def _decrypt_result(self, HE, res):
        res.decrypt(HE)
        return res.toLogs()
    
    def _send_result(self, service, resultLogs):
        index = service.indexes[self.result_index]
        i=0
        for result in resultLogs:
            i += 1
            print(result)
            index.submit(result, sourcetype=self.sourcetype)
        print(i)

class HashReport(Report):
    def __init__(self):
        self.search='search index=hashes | head 5'
        
        self.create_dict = dict()
        self.create_dict['rf'] = "hash"
        self.create_dict['earliest_time'] = "-1m"
        
        self.results_dict = dict()
        self.results_dict['count'] = 0
        self.results_dict['output_mode'] = "json"
        self.results_dict['field_list'] = "_raw hash"

        self.result_index = "result_hashes"
        self.sourcetype = 'hash-check'
    
    def _prepare_operation(self, HE, search_result):
        hashes_to_check = []
        
        for result in search_result:
            print("search res:", result)
            hashes_to_check += [
                result['hash']
            ]
        
        operation = FindMaliciousHashesOperation(hashes_to_check)
        operation.encrypt(HE)

        return operation

class IpReport(Report):
    def __init__(self):
        self.search='search index=ips | head 5'
        
        self.create_dict = dict()
        self.create_dict['rf'] = "ip"
        self.create_dict['earliest_time'] = "-1m"
        
        self.results_dict = dict()
        self.results_dict['count'] = 0
        self.results_dict['output_mode'] = "json"
        self.results_dict['field_list'] = "_raw ip"

        self.result_index = "result_ips"
        self.sourcetype = 'ip-check'
    
    def _getHEContext(self):
        if os.path.exists('HE_context_and_keys_counting_and_groupping'):
            HE = PyfhelUtils.loadHE('HE_context_and_keys_counting_and_groupping')
            return HE

        HE = Pyfhel()
        HE.contextGen(scheme='bfv', n=2**15, t_bits=17)
        HE.keyGen()
        
        PyfhelUtils.saveHE('HE_context_and_keys_counting_and_groupping', HE)

        return HE
    
    def _prepare_operation(self, HE, search_result):
        ips_to_count = []
        
        for result in search_result:
            print("ip search res:", result)
            ips_to_count += [
                result['ip']
            ]
        
        operation = IpGroupAndCountOperation(ips_to_count)
        operation.encrypt(HE)

        return operation

def main():
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} [reportType]")
        sys.exit(1)

    reportType = sys.argv[1]

    if reportType == "hash":
        report = HashReport()
    elif reportType == "ip":
        report = IpReport()
    else:
        print(f"Incorrect report type. Allowed: hash, ip")
        sys.exit(1)
    
    load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    username = os.getenv('username')
    password = os.getenv('password')

    service = client.connect(host=host, port=port, username=username, password=password)
    assert isinstance(service, client.Service)
    
    report.generate(service)

if __name__ == "__main__":
    main()
