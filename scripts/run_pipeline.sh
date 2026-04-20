#!/bin/bash

echo "🏭 Starting Continuous Factory Pipeline..."

while true; do
    # 1. Check if there are any CSV files waiting in HDFS
    FILES=$(docker exec namenode hdfs dfs -ls /iot/input/raw 2>/dev/null | grep "\.csv")
    
    if [ -z "$FILES" ]; then
        echo "⏳ No new data in HDFS. Waiting 5 seconds..."
        sleep 5
        continue
    fi

    # Create a unique timestamp for the output folder
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    OUT_DIR="/iot/output/run_$TIMESTAMP"

    echo "🚀 Found new data! Starting MapReduce Job: run_$TIMESTAMP..."
    
    # 2. Run MapReduce on ALL files currently in the raw folder
    # (We hide the massive wall of logs using > /dev/null so the terminal stays clean)
    docker exec namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
      -files /iot_data/mr_scripts/mapper.py,/iot_data/mr_scripts/reducer.py \
      -mapper "python3 mapper.py" \
      -reducer "python3 reducer.py" \
      -input /iot/input/raw/*.csv \
      -output $OUT_DIR > /dev/null 2>&1

    # 3. Check if the job was successful
    if [ $? -eq 0 ]; then
        echo "✅ MapReduce finished!"
        
        # Pull the results and save them locally
        docker exec namenode hdfs dfs -cat $OUT_DIR/part-00000 > ../data/temp_results.txt
        
        # Merge the new results into your master JSON file
        python3 merge_state.py ../data/temp_results.txt
        
        # 4. Clean up: Move the processed files to an archive folder in HDFS
        docker exec namenode hdfs dfs -mkdir -p /iot/archive
        docker exec namenode hdfs dfs -mv /iot/input/raw/*.csv /iot/archive/
        echo "🧹 Cleaned up processed files."
        
    else
        echo "❌ Job failed or is recovering from a node failure..."
    fi
    
    echo "-----------------------------------"
    sleep 2
done
