# Splunk-App-for-homomorphic-encryption

## Logs generators

1. ```esxi_log_generator.py```

    This script generates logs which imitate failed login attempts to VMware ESXi. 

    `Usage: python3 esxi_logs_generator.py [OPTIONS...]`

1. ```hashes_generator.py```

    This script generates logs which imitate transfer of files with their hashes. 

    `Usage: python3 hashes_generator.py [OPTIONS...]`

General Options for both scripts
```
-h, --help           Prints a short help text and exists
-d, --days <value>   Set number of days in past to generate logs. Default 0
-f, --file <path>    Set log file. Default /var/log/esxi.log
-s, --stop           Don't generate logs continuously
```

# Running

1. Install dependencies

    `pip install -r requirements.txt`

1. Install Splunk

1. Setup Splunk
    - add generated logs
    - generated hashes add to new index `hashes`
    - create field extractor for hashes using regex `hostname: (?<hostname>.*) ip:(?<ip>.*) path:(?<file>.*) sha256:(?<hash>[0-9a-fA-F]{64})`
    - create index `result_hashes` for results
    - (optional) create field exractor for result_hashes using regex `(?<=hash: )(?<hash>[0-9a-fA-F]{64}).*?: (?<is_malicious>(False|True))`

1. Generate logs using above scripts

1. Set Splunk server settings  
    - `cp .env.example .env`
    - set correct values in .env file

1. Run `python hash_report.py`  
    It will fetch logs from Splunk and generate file `fileA.pickle` that contains requested operations & encrypted data

1. In other terminal run `python ./processor.py fileA.pickle fileB.pickle`  
    It will run requested operations on provided encrypted data. Result will be saved in `fileB.pickle`

1. Press enter in the first terminal  
    It will read results from `fileB.pickle` and send logs back to Splunk
