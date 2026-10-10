from typing import List
from core.models import Process, ProcessMetrics, GanttSegment, SimulationResult
from core.metrics import calculate_overall_metrics, merge_gantt_segments

def simulate(processes: List[Process], **kwargs) -> SimulationResult:
    processes = sorted(processes, key=lambda x: (x.at, x.pid))
    current_time = 0
    gantt = []
    metrics = []
    
    for p in processes:
        if current_time < p.at:
            gantt.append(GanttSegment("IDLE", current_time, p.at))
            current_time = p.at
            
        start_time = current_time
        gantt.append(GanttSegment(p.pid, start_time, start_time + p.bt))
        current_time += p.bt
        
        ct = current_time
        tat = ct - p.at
        wt = tat - p.bt
        rt = start_time - p.at
        
        metrics.append(ProcessMetrics(p.pid, p.at, p.bt, p.priority, ct, tat, wt, rt))
        
    gantt = merge_gantt_segments(gantt)
    overall = calculate_overall_metrics(metrics, gantt)
    
    return SimulationResult(
        processes=metrics,
        gantt=gantt,
        **overall
    )
