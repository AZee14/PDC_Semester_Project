# 🏭 Industrial IoT Distributed Log Processing System

A fault-tolerant, distributed Big Data pipeline that simulates real-time Industrial IoT analytics. This system ingests simulated continuous sensor data, stores it across a distributed file system (HDFS), processes it in parallel using Hadoop MapReduce, and visualizes the aggregated metrics on a live dashboard.

-----

## 🚀 How to Run This on Your System

**⚠️ Prerequisites:** You MUST have **WSL (Ubuntu)**, **Hadoop**, and **Docker Desktop** installed and running on your machine before starting.

### Step 1: Get the Code & Setup Folders

Open your WSL terminal and clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Create the necessary local directories
mkdir -p data/staging data/archive data/mr_scripts
```

*(Note: Replace `YOUR_USERNAME/YOUR_REPO_NAME` with your actual GitHub details).*

### Step 2: Turn on the Hadoop Cluster

Boot up the distributed Docker network:

```bash
docker compose up -d
```

> **Verify:** Wait a few minutes for the images to download and start. Check [http://localhost:9870](https://www.google.com/search?q=http://localhost:9870) in your browser. Go to the "Datanodes" tab to verify exactly **3 Live Nodes** are running.

### Step 3: Setup the Hadoop Internal Folders & Python

Run these commands to prepare the Hadoop Distributed File System (HDFS) and install Python on the master node so it can execute our MapReduce logic:

```bash
docker exec namenode hdfs dfs -mkdir -p /iot/input/raw
docker exec namenode hdfs dfs -mkdir -p /iot/output
docker exec -u root namenode bash -c "echo 'deb http://archive.debian.org/debian buster main' > /etc/apt/sources.list && apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y python3"
```

### Step 4: Start the Factory (The Pipeline)

To simulate the factory, you need to open **4 separate WSL tabs**. In each tab, navigate to the `scripts` folder (`cd scripts`) and run the following commands one by one:

  * **Tab 1 (The Streamer):** Generates the simulated sensor data.
    ```bash
    python3 stream_simulator.py
    ```
  * **Tab 2 (The Ingestor):** Pushes the local micro-batches into HDFS.
    ```bash
    ./ingest.sh
    ```
  * **Tab 3 (The Brains):** Orchestrates the MapReduce jobs and merges the state.
    ```bash
    ./run_pipeline.sh
    ```
  * **Tab 4 (The Face):** Starts the Streamlit User Interface.
    ```bash
    python3 -m streamlit run dashboard.py
    ```

🎉 **View the Dashboard:** Go to [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501) to see the live analytics\!

> **💥 The Chaos Test (Fault Tolerance):** To prove the system survives hardware failure, open a 5th terminal tab while the system is running and type `docker stop datanode2`. Watch the dashboard seamlessly recover and continue updating\!

-----

## ⚙️ Dataset Generation & Architecture

### 1\. The Dataset (The "What" and "Why")

The `generate_dataset.py` script creates a simulated factory dataset. Every single row represents a single "ping" or reading from a factory machine at a specific second in time.

The data looks like this:

```text
2026-04-20 14:05:01, MACH-004, 86.5, ERROR, E-99
```

**Real-World Scenario Mapping:**

  * `machine_id`: The factory contains 10 machines (`MACH-001` to `MACH-010`).
  * `temperature`: The script randomly generates a temperature reading for each machine.
  * `error_code`: Hardcoded logic dictates that if a machine's temperature randomly spikes above 85°C, it forces an `E-99` (Overheating) error.

**Why we simulate streaming:**
In a real factory, you don't get a massive Excel file at the end of the day. Machines send data continuously. Our `stream_simulator.py` mimics this reality by chopping the massive dataset into tiny "micro-batches" (100 rows at a time) and dripping them into the system every 5 seconds.

### 2\. What MapReduce Accomplishes (The "Brain")

MapReduce is Google's famous algorithm for processing massive amounts of data across multiple computers without crashing. Instead of asking one computer to read a million rows, MapReduce splits the work into two phases.

#### 🔹 Phase 1: The Mapper (The "Extractor")

The Mapper looks at the raw data line-by-line. Its only job is to filter out the noise and extract what we care about: Errors. If it reads a line where `MACH-004` has an `E-99` error, it immediately outputs two separate key-value tags:

> `ERR_MACHINE_MACH-004    1`  *(Translation: "I found 1 error for Machine 4\!")*
> `ERR_CODE_E-99           1`  *(Translation: "I found 1 E-99 error\!")*

Because you have 3 DataNodes, multiple Mappers do this simultaneously across different chunks of the data file.

#### 🔹 Phase 2: The Reducer (The "Calculator")

Hadoop takes all those scattered "1s", sorts them, and hands them to the Reducer. The Reducer acts as an aggregator:

> *"I see six 1s for MACH-004. Output -\> `ERR_MACHINE_MACH-004: 6`."*
> *"I see twenty-eight 1s for E-99. Output -\> `ERR_CODE_E-99: 28`."*

**🏆 The Ultimate Goal:** By extracting in parallel (Map) and aggregating the final math (Reduce), MapReduce allows the system to process terabytes of factory logs in seconds, turning messy sensor data into the clean, summarized JSON numbers that power the dashboard.

-----

## 🔐 GitHub Authentication (Required for Contributing)

In 2021, GitHub removed the ability to use your account password to push code from the terminal. If you try to run `git push` with your normal password, you will get an `Authentication failed` error.

To push code to this repository, you must generate a **Personal Access Token (PAT)**.

### How to set up your Token:

1.  Log in to [GitHub.com](https://github.com/).
2.  Go to **Settings** (click your profile picture in the top right).
3.  Scroll down the left menu and click **Developer settings** -\> **Personal access tokens** -\> **Tokens (classic)**.
4.  Click **Generate new token (classic)**.
5.  Name it something like "WSL Project Token" and set the expiration to 30 or 90 days.
6.  **Important:** Check the box next to **`repo`** to give it permission to push code.
7.  Click **Generate** at the bottom and **copy the token immediately** (it starts with `ghp_`).

### How to use it:

When you run your first `git push`, the terminal will ask for your username and password.

  * **Username:** Your GitHub username
  * **Password:** *Paste your new token here (Ctrl+Shift+V or Right-Click).* \> *Note: Linux hides passwords as you type, so nothing will show up on the screen. Just paste it and press Enter.*

### 💡 Pro-Tip: Don't enter it every time\!

To force Git to remember your token so you never have to paste it again, run this command in your terminal *before* you push:

```bash
git config --global credential.helper store
```
