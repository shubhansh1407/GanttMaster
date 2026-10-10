from typing import List
from core.models import Process, ProcessMetrics, GanttSegment, SimulationResult
from core.metrics import calculate_overall_metrics, merge_gantt_segments

def simulate(processes: List[Process], tq: int = 2, **kwargs) -> SimulationResult:
    n = len(processes)
    completed = 0
    current_time = 0
    gantt = []
    
    remaining_bt = {p.pid: p.bt for p in processes}
    first_start = {}
    completion_times = {}
    
    processes_sorted = sorted(processes, key=lambda x: (x.at, x.pid))
    ready_queue = []
    arrived_idx = 0
    
    # Enqueue processes arriving at t=0
    while arrived_idx < n and processes_sorted[arrived_idx].at <= current_time:
        ready_queue.append(processes_sorted[arrived_idx])
        arrived_idx += 1
        
    while completed < n:
        if not ready_queue:
            next_at = processes_sorted[arrived_idx].at
            gantt.append(GanttSegment("IDLE", current_time, next_at))
            current_time = next_at
            while arrived_idx < n and processes_sorted[arrived_idx].at <= current_time:
                ready_queue.append(processes_sorted[arrived_idx])
                arrived_idx += 1
                
        p = ready_queue.pop(0)
        
        if p.pid not in first_start:
            first_start[p.pid] = current_time
            
        run_time = min(remaining_bt[p.pid], tq)
        
        gantt.append(GanttSegment(p.pid, current_time, current_time + run_time))
        current_time += run_time
        remaining_bt[p.pid] -= run_time
        
        # Enqueue new arrivals
        while arrived_idx < n and processes_sorted[arrived_idx].at <= current_time:
            ready_queue.append(processes_sorted[arrived_idx])
            arrived_idx += 1
            
        # Re-enqueue the preempted process
        if remaining_bt[p.pid] > 0:
            ready_queue.append(p)
        else:
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
