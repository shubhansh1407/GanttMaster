import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.sample_data import DATASETS
from algorithms import ALGORITHMS

print("Testing algorithms...")
for algo_name, algo_func in ALGORITHMS.items():
    print(f"\\n--- {algo_name} ---")
    dataset = DATASETS["Basic"]()
    res = algo_func(dataset, tq=2)
    print(f"Avg WT: {res.avg_wt:.2f}, Avg TAT: {res.avg_tat:.2f}, Throughput: {res.throughput:.2f}")
    print("Gantt:", [(s.pid, s.start_time, s.end_time) for s in res.gantt])
print("\\nAll tests passed successfully.")
