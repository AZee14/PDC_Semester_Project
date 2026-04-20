#!/usr/bin/env python3
import sys
import csv

# Read from standard input (which Hadoop uses to pass data)
reader = csv.reader(sys.stdin)

for row in reader:
    # Skip empty lines or the CSV header
    if not row or row[0] == "timestamp":
        continue
        
    machine_id = row[1]
    status = row[3]
    error_code = row[4]
    
    # 1. If there's an error, count it for this specific machine
    if status == "ERROR":
        print(f"ERR_MACHINE_{machine_id}\t1")
    
    # 2. Count the frequency of the specific error code
    if error_code != "NONE":
        print(f"ERR_CODE_{error_code}\t1")
        
    # 3. Count total records processed
    print(f"TOTAL_RECORDS\t1")
