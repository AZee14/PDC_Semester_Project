import streamlit as st
import pandas as pd
import json
import time
import os

# 1. Setup the webpage layout
st.set_page_config(page_title="IoT Factory Dashboard", layout="wide")
STATE_FILE = "../data/master_state.json"

# 2. Create a placeholder that we will overwrite every few seconds
placeholder = st.empty()

# 3. Endless loop to keep the dashboard updating live
while True:
    # Safely load the JSON file
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except json.JSONDecodeError:
            state = {"TOTAL_RECORDS": 0} # Fallback if file is mid-write
    else:
        state = {"TOTAL_RECORDS": 0}

    # Separate the data into lists for our charts
    machines = {"Machine": [], "Error Count": []}
    codes = {"Error Code": [], "Frequency": []}
    total_records = state.get("TOTAL_RECORDS", 0)

    for key, value in state.items():
        if key.startswith("ERR_MACHINE_"):
            machines["Machine"].append(key.replace("ERR_MACHINE_", ""))
            machines["Error Count"].append(value)
        elif key.startswith("ERR_CODE_"):
            codes["Error Code"].append(key.replace("ERR_CODE_", ""))
            codes["Frequency"].append(value)

    # Convert to Pandas DataFrames for Streamlit
    df_machines = pd.DataFrame(machines)
    df_codes = pd.DataFrame(codes)

    # 4. Draw the UI inside the placeholder
    with placeholder.container():
        st.title("Live Industrial IoT Dashboard")
        st.markdown("Monitoring distributed Hadoop cluster processing in real-time.")
        
        # Big metric number
        st.metric(label="Total Sensor Records Processed", value=total_records)
        
        st.divider()

        # Two columns for side-by-side charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Errors per Machine")
            if not df_machines.empty:
                st.bar_chart(df_machines.set_index("Machine"))
            else:
                st.info("Waiting for machine data...")

        with col2:
            st.subheader("Error Code Frequency")
            if not df_codes.empty:
                st.bar_chart(df_codes.set_index("Error Code"))
            else:
                st.info("Waiting for error code data...")

    # Wait 3 seconds, then force Streamlit to rerun the script and update the data
    time.sleep(3)
    st.rerun()
