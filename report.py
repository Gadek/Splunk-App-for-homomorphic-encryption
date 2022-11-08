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
    def __init__(self, timeFrom, timeTo, sourceIndex):
        self.source_index = ''
        self.result_index = ''
        self.earliest_time = timeFrom
        self.latest_time = timeTo
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
        if len(resultLogs)>0:
            self._send_result(service, resultLogs)
    
    def _perform_search(self, service):
        search = 'search index=' + self.source_index + '|dedup hash | where isNull(malicious)'
        create_dict = dict()
        create_dict['rf'] = "hash"
        create_dict['earliest_time'] = self.earliest_time
        create_dict['latest_time'] = self.latest_time
        results_dict = dict()
        results_dict['count'] = 0
        results_dict['output_mode'] = "json"
        results_dict['field_list'] = "_raw hash"

        job = service.jobs.create(search, **create_dict)

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
    
    def _getHEContext(self):
        if os.path.exists('HE_context_and_keys/basic'):
            HE = PyfhelUtils.loadHE('HE_context_and_keys/basic')
            return HE

        HE = Pyfhel()
        HE.contextGen(scheme='bfv', n=2**15, t_bits=34)
        HE.keyGen()
        
        PyfhelUtils.saveHE('HE_context_and_keys/basic', HE)

        return HE
    
    def _prepare_operation(self, HE, search_result):
        raise NotImplementedError("Please Implement this method")
    
    def _decrypt_result(self, HE, res):
        res.decrypt(HE)
        return res.toLogs()
    
    def _send_result(self, service, resultLogs):
        print("_raw,hash,malicious")
        for result in resultLogs:
            print(result.split(',')[0],result.split(',')[1][:-1],",",result[:-1])
        search = '| makeresults format=csv data="hash,malicious\n' + "".join(resultLogs) +'" | outputlookup append=True hashes'

        job = service.jobs.create(search)

        while True:
            while not job.is_ready():
                pass
            if job['isDone'] == '1':
                break
            sleep(2)

class HashReport(Report):
    def __init__(self, timeFrom, timeTo, sourceIndex):
        super().__init__(timeFrom, timeTo, sourceIndex)
        self.source_index = sourceIndex

    
    def _prepare_operation(self, HE, search_result):
        hashes_to_check = []
        
        for result in search_result:
            #print("search result:", result['_raw'])
            hashes_to_check += [
                result['hash']
            ]
        
        operation = FindMaliciousHashesOperation(hashes_to_check)
        operation.encrypt(HE)

        return operation

class IpReport(Report):
    def __init__(self, timeFrom, timeTo, sourceIndex):
        super().__init__(timeFrom, timeTo, sourceIndex)
        self.source_index = sourceIndex
        self.result_index = 'result_ips'
        self.sourcetype = 'ip-check'
    
    def _getHEContext(self):
        if os.path.exists('HE_context_and_keys/counting_and_groupping'):
            HE = PyfhelUtils.loadHE('HE_context_and_keys/counting_and_groupping')
            return HE

        HE = Pyfhel()
        HE.contextGen(scheme='bfv', n=2**15, t_bits=17)
        HE.keyGen()
        HE.relinKeyGen()
        HE.rotateKeyGen()
        
        PyfhelUtils.saveHE('HE_context_and_keys/counting_and_groupping', HE)

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
    if len(sys.argv) <= 4:
        print(f"Usage: {sys.argv[0]} [reportType] [timeFrom] [timeTo] [sourceIndex]")
        sys.exit(1)

    reportType = sys.argv[1]
    timeFrom = sys.argv[2]
    timeTo = sys.argv[3]
    sourceIndex = sys.argv[4]

    if reportType == "hash":
        report = HashReport(timeFrom, timeTo, sourceIndex)
    elif reportType == "ip":
        report = IpReport(timeFrom, timeTo, sourceIndex)
    else:
        print(f"Incorrect report type. Allowed: hash, ip")
        sys.exit(1)
    
    load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    # username = os.getenv('username')
    # password = os.getenv('password')
    token = os.getenv('token')

    # service = client.connect(host=host, port=port, username=username, password=password)
    service = client.connect(host=host, port=port, token=token)
    assert isinstance(service, client.Service)
    
    report.generate(service)

if __name__ == "__main__":
    main()
