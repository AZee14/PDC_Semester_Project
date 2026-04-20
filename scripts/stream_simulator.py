import csv
import time
import os
from datetime import datetime

INPUT_FILE = "../data/raw_iot_data.csv"
STAGING_DIR = "../data/staging/"
BATCH_SIZE = 100  # How many records per batch
SLEEP_TIME = 5    # Seconds between batches

print("🚀 Starting IoT Sensor Simulator...")
print(f"Dropping {BATCH_SIZE} records every {SLEEP_TIME} seconds.")
print("Press Ctrl+C to stop.")

try:
    with open(INPUT_FILE, 'r') as file:
        reader = csv.reader(file)
        header = next(reader) # skip header
        
        batch_num = 1
        current_batch = []
        
        for row in reader:
            current_batch.append(row)
            
            if len(current_batch) == BATCH_SIZE:
                # Create a unique filename based on time
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(STAGING_DIR, f"batch_{timestamp}_{batch_num}.csv")
                
                with open(filename, 'w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    writer.writerows(current_batch)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📦 Dropped batch {batch_num} into staging.")
                
                # Reset for next batch and wait
                current_batch = []
                batch_num += 1
                time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("\n🛑 Simulator stopped by user.")
