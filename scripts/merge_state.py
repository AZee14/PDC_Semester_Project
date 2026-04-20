import json
import os
import sys

STATE_FILE = "../data/master_state.json"

# We will pass the downloaded Hadoop output file as an argument
if len(sys.argv) < 2:
    print("❌ Error: Please provide the path to the MapReduce output file.")
    sys.exit(1)

NEW_DATA_FILE = sys.argv[1]

# 1. Load the existing master state (if it exists)
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
else:
    state = {"TOTAL_RECORDS": 0} # Start fresh

# 2. Read the new MapReduce output
with open(NEW_DATA_FILE, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # Split the KEY and VALUE (which are separated by a tab)
        parts = line.split('\t')
        if len(parts) == 2:
            key = parts[0]
            count = int(parts[1])
            
            # Add the new count to the existing total for this key
            state[key] = state.get(key, 0) + count

# 3. Save the updated master state
with open(STATE_FILE, 'w') as f:
    json.dump(state, f, indent=4)

print("✅ Master state updated successfully! Current Total Records:", state["TOTAL_RECORDS"])
