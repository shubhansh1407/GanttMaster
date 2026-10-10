from typing import List
from core.models import Process, ProcessMetrics, GanttSegment, SimulationResult
from core.metrics import calculate_overall_metrics, merge_gantt_segments

def simulate(processes: List[Process], **kwargs) -> SimulationResult:
    n = len(processes)
    completed = 0
    current_time = 0
    gantt = []
    metrics = []
    
    is_completed = {p.pid: False for p in processes}
    
    while completed < n:
        arrived = [p for p in processes if p.at <= current_time and not is_completed[p.pid]]
        
        if not arrived:
            next_at = min(p.at for p in processes if not is_completed[p.pid])
            gantt.append(GanttSegment("IDLE", current_time, next_at))
            current_time = next_at
            continue
            
        # Select highest priority (lower number), tie breaker AT then PID
        arrived.sort(key=lambda x: (x.priority, x.at, x.pid))
        p = arrived[0]
        
        start_time = current_time
        gantt.append(GanttSegment(p.pid, start_time, start_time + p.bt))
        current_time += p.bt
        
        ct = current_time
        tat = ct - p.at
        wt = tat - p.bt
        rt = start_time - p.at
        
        metrics.append(ProcessMetrics(p.pid, p.at, p.bt, p.priority, ct, tat, wt, rt))
        is_completed[p.pid] = True
        completed += 1
        
    gantt = merge_gantt_segments(gantt)
    overall = calculate_overall_metrics(metrics, gantt)
    
    return SimulationResult(
        processes=metrics,
        gantt=gantt,
        **overall
    )
