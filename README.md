# GanttMaster: CPU Scheduling Visualizer

## Simulating • Visualizing • Comparing CPU Scheduling Algorithms

This is a Computer Organization and Operating Systems (COOS) mini project. It provides a visual, interactive simulation of fundamental CPU scheduling algorithms.

## Objective
To build a fully functional application that takes a workload of processes and demonstrates how different CPU scheduling algorithms process them, complete with Gantt charts and performance metrics comparison.

## Algorithms Implemented
1. **First Come First Serve (FCFS)**
2. **Shortest Job First (SJF)**
3. **Shortest Remaining Time First (SRTF)**
4. **Priority Scheduling**
5. **Round Robin (RR)**

## Metrics Calculated
- Arrival Time (AT)
- Burst Time (BT)
- Completion Time (CT)
- Turnaround Time (TAT)
- Waiting Time (WT)
- Response Time (RT)
- CPU Utilization
- Throughput

## Technology Stack
- **Python**: Core logic
- **Streamlit**: Web interface
- **Pandas**: Data handling
- **Matplotlib**: Gantt charts and data visualization

## Project Structure
```
cpu-scheduling-visualizer/
├── app.py                  # Main Streamlit application
├── algorithms/             # Implementation of all scheduling algorithms
├── core/                   # Shared models, metrics, and simulator utilities
├── visualization/          # Gantt chart and comparison plotting logic
├── data/                   # Sample datasets
└── requirements.txt        # Dependencies
```

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run app.py
   ```

## Future Scope
- Add Multi-level Queue Scheduling.
- Support importing workloads from CSV files.
- Export simulation reports to PDF.
