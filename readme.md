# Distributed Matrix Multiplication Benchmarking 

**Big Data Course - Task 4** **University of Las Palmas de Gran Canaria (ULPGC)** **Student:** Mariana Bordes Bueno

## Overview

This project implements and benchmarks **Distributed Matrix Multiplication** algorithms using the **Master-Worker** pattern (inspired by the MapReduce paradigm). The primary goal is to evaluate the performance trade-offs between computational parallelism and network overhead.

The study compares three execution modes:
1.  **Basic:** Sequential execution ($O(N^3)$).
2.  **Parallel:** Multi-threaded execution (Java Streams / Python Multiprocessing).
3.  **Distributed:** Networked execution across multiple nodes.

Two distinct implementations were developed to analyze different levels of abstraction:
* **Java:** Using **Hazelcast** (High-level middleware for cluster management).
* **Python:** Using raw **Sockets & Multiprocessing** (Low-level custom protocol).

## Project Structure

The project is organized into two main source modules and an analysis folder:

```text
├── java-src/
│   ├── Main.java                        # Entry point for Java benchmarks
│   ├── DistributedMatrixMultiplication.java # Master node logic (Hazelcast)
│   ├── MatrixMultiplicationTask.java    # Serializable task sent to Workers
│   ├── WorkerNode.java                  # Standalone Worker executable
│   ├── BasicMatrixMultiplication.java   # Baseline sequential algorithm
│   ├── ParallelMatrixMultiplication.java# Local parallel (Stream) algorithm
│   ├── MatrixMultiplier.java            # Common interface
│   └── CSVWriterUtility.java            # Helper for CSV export
│
├── python-src/
│   ├── main_benchmark_v2.py             # Entry point (Master + Benchmark loop)
│   ├── distributed_worker.py            # Worker logic (Sockets)
│   └── matrix_utils.py                  # Matrix generation and local algos
│
├── analysis/
│   ├── generate_plots.py                # Python script to generate graphs
│   └── generate_extra_plots.py          # Script for Speedup/Efficiency plots
│
└── results/
    ├── benchmark_results.csv            # Java output data
    ├── python_benchmark_results.csv     # Python output data
    └── plots/                           # Generated PNG visualizations
```
## Prerequisites
Java Environment
- JDK: Version 19 or higher.
- Library: com.hazelcast:hazelcast:5.3.0

Python Environment
- Python: Version 3.10+.
- Dependencies: Install the required libraries for benchmarking and plotting:
```bash
pip install numpy pandas psutil matplotlib seaborn
````
## How to Run
### Java Implementation (Hazelcast)
To correctly simulate a distributed environment with 2 Nodes (Master + 1 Worker) on a single machine, follow this specific order.

**Step 1: Start the Worker Node Open a terminal, compile the Java files, and run the WorkerNode class. It will start a Hazelcast instance and wait for tasks.**
```bash
cd java-src
# Compile (Windows/Linux separator may vary: use ; for Windows, : for Linux/Mac)
javac -cp ".:hazelcast-5.3.0.jar" *.java
# Run Worker
java -cp ".:hazelcast-5.3.0.jar" WorkerNode
````
(Wait until you see Members [1] in the console).

**Step 2: Run the Benchmark (Master) Open a second terminal and run the Main class.**

```bash
cd java-src
java -cp ".:hazelcast-5.3.0.jar" Main
````

The Master will detect the Worker (console will show Members [2]), distribute the workload, and generate benchmark_results.csv in the project root.

### Python Implementation (Sockets)
The Python implementation automatically handles the creation and termination of worker processes via subprocess. No manual worker startup is required.

1. Navigate to the python source folder:

```bash
cd python-src
````
2. Run the main benchmark script:
```bash
python main_benchmark_v2.py
````
This will execute Basic, Parallel, and Distributed benchmarks for sizes N=500, 1000, 2000 and generate python_benchmark_results.csv.

## Visualizing Results
Once both benchmarks are finished and the .csv files are generated in the root directory:

1. Run the plotting script to generate the analysis graphs:

```bash
python analysis/generate_plots.py
```
2. (Optional) Run the advanced metrics script for Speedup and Efficiency analysis:

```bash
python analysis/generate_extra_plots.py
```
3. Check the results/plots/ directory for the generated PNG images used in the report.
