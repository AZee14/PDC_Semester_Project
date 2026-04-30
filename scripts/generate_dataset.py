# Simulate factory 
import csv
import random
from datetime import datetime, timedelta

# Config
NUM_RECORDS = 50000
OUTPUT_FILE = "../data/raw_iot_data.csv" 
MACHINE_IDS = [f"MACH-{i:03d}" for i in range(1, 11)] # 10 machines
STATUSES = ["OK", "OK", "OK", "OK", "WARNING", "ERROR"] 
ERRORS = ["NONE", "NONE", "NONE", "E-01", "E-02", "E-03", "E-99"]

print(f"Generating {NUM_RECORDS} sensor records...")

# Generate Raw Data With Error
with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["timestamp", "machine_id", "temperature", "status", "error_code"])
    
    current_time = datetime.now()
    # Generate records 
    for _ in range(NUM_RECORDS):
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        machine = random.choice(MACHINE_IDS)
        
        # Base temp around 70C, random variation
        temp = round(random.uniform(65.0, 90.0), 2)
        
        status = random.choice(STATUSES)
        error = random.choice(ERRORS) if status != "OK" else "NONE"
        
        # If it's too hot, force a warning/error
        if temp > 85.0:
            status = "ERROR"
            error = "E-99" # Overheating error
            
        writer.writerow([timestamp, machine, temp, status, error])
        
        # Advance time slightly for the next record
        current_time += timedelta(seconds=random.randint(1, 5))

print(f"Done! Dataset saved to {OUTPUT_FILE}")
