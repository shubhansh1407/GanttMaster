from typing import List
from core.models import Process, ProcessMetrics, GanttSegment, SimulationResult
from core.metrics import calculate_overall_metrics, merge_gantt_segments

def simulate(processes: List[Process], **kwargs) -> SimulationResult:
    n = len(processes)
    completed = 0
    current_time = 0
    gantt = []
    
    remaining_bt = {p.pid: p.bt for p in processes}
    first_start = {}
    completion_times = {}
    
    while completed < n:
        arrived = [p for p in processes if p.at <= current_time and remaining_bt[p.pid] > 0]
        
        if not arrived:
            next_at = min(p.at for p in processes if remaining_bt[p.pid] > 0)
            gantt.append(GanttSegment("IDLE", current_time, next_at))
            current_time = next_at
            continue
            
        # Select shortest remaining time, tie breaker AT then PID
        arrived.sort(key=lambda x: (remaining_bt[x.pid], x.at, x.pid))
        p = arrived[0]
        
        if p.pid not in first_start:
            first_start[p.pid] = current_time
            
        future_arrivals = [x.at for x in processes if x.at > current_time and remaining_bt[x.pid] > 0]
        if future_arrivals:
            next_arrival = min(future_arrivals)
            run_time = min(remaining_bt[p.pid], next_arrival - current_time)
        else:
            run_time = remaining_bt[p.pid]
            
        gantt.append(GanttSegment(p.pid, current_time, current_time + run_time))
        current_time += run_time
        remaining_bt[p.pid] -= run_time
        
        if remaining_bt[p.pid] == 0:
            completion_times[p.pid] = current_time
            completed += 1
            
    metrics = []
    for p in processes:
        ct = completion_times[p.pid]
        tat = ct - p.at
        wt = tat - p.bt
        rt = first_start[p.pid] - p.at
        metrics.append(ProcessMetrics(p.pid, p.at, p.bt, p.priority, ct, tat, wt, rt))
        
    gantt = merge_gantt_segments(gantt)
    overall = calculate_overall_metrics(metrics, gantt)
    
    return SimulationResult(
        processes=metrics,
        gantt=gantt,
        **overall
    )
