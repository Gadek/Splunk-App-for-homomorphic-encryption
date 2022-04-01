# Splunk-App-for-homomorphic-encryption

```esxi_log_generator.py```
This script generates logs which imitate failed login attempts to VMware ESXi. 

    Usage: python3 esxi_logs_generator.py [OPTIONS...] 
    General Options 
    -h, --help           Prints a short help text and exists
    -d, --days <value>   Set number of days in past to generate logs. Default 0
    -f, --file <path>    Set log file. Default /var/log/esxi.log
