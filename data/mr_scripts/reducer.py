#!/usr/bin/env python3
import sys

current_key = None
current_count = 0

# Read from standard input
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    # Split the line into the key and the count (which is always 1 from our mapper)
    key, count = line.split('\t', 1)
    
    try:
        count = int(count)
    except ValueError:
        continue
        
    # If we are still reading the same key, keep adding to the total
    if current_key == key:
        current_count += count
    else:
        # If the key changed, print the final total for the PREVIOUS key
        if current_key:
            print(f"{current_key}\t{current_count}")
        current_key = key
        current_count = count

# Don't forget to print the very last key!
if current_key == key:
    print(f"{current_key}\t{current_count}")
