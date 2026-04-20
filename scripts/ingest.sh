#!/bin/bash

STAGING_DIR="../data/staging"
ARCHIVE_DIR="../data/archive"
HDFS_DIR="/iot/input/raw"

echo "🚀 Starting HDFS Ingestion Pipeline..."
echo "👀 Monitoring $STAGING_DIR for new micro-batches..."

while true; do
    # Loop through any CSV files in the staging directory
    for filepath in "$STAGING_DIR"/*.csv; do
        
        # If no CSV files exist, the loop will literally see '*.csv', so we skip it
        [ -e "$filepath" ] || continue
        
        filename=$(basename "$filepath")
        echo "📦 Found $filename! Uploading to HDFS..."
        
        # 1. Instruct the NameNode to put the file into HDFS
        # (It uses /iot_data because that is how the volume is mounted inside Docker)
        docker exec namenode hdfs dfs -put "/iot_data/staging/$filename" "$HDFS_DIR/"
        
        # 2. Move the local file to the archive folder
        mv "$filepath" "$ARCHIVE_DIR/"
        
        echo "✅ Upload complete and file archived."
    done
    
    # Pause for 3 seconds before checking the folder again
    sleep 3
done
