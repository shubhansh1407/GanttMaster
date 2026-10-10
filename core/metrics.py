from typing import List, Dict, Any
from core.models import ProcessMetrics, GanttSegment, SimulationResult

def calculate_overall_metrics(metrics: List[ProcessMetrics], gantt: List[GanttSegment]) -> Dict[str, Any]:
    """Calculates overall metrics from a list of ProcessMetrics and Gantt chart segments."""
    if not metrics:
        return {
            "avg_wt": 0.0,
            "avg_tat": 0.0,
            "avg_rt": 0.0,
            "cpu_utilization": 0.0,
            "throughput": 0.0,
            "total_time": 0,
            "idle_time": 0
        }
        
    avg_wt = sum(m.wt for m in metrics) / len(metrics)
    avg_tat = sum(m.tat for m in metrics) / len(metrics)
    avg_rt = sum(m.rt for m in metrics) / len(metrics)
    
    start_time = min(m.at for m in metrics)
    if not gantt:
        end_time = start_time
        total_time = 0
        busy_time = 0
    else:
        end_time = max(s.end_time for s in gantt)
        total_time = end_time - start_time
        busy_time = sum(s.duration for s in gantt if s.pid != "IDLE")
        
    idle_time = total_time - busy_time if total_time > 0 else 0
    cpu_utilization = (busy_time / total_time * 100) if total_time > 0 else 0.0
    throughput = (len(metrics) / total_time) if total_time > 0 else 0.0
    
    return {
        "avg_wt": avg_wt,
        "avg_tat": avg_tat,
        "avg_rt": avg_rt,
        "cpu_utilization": cpu_utilization,
        "throughput": throughput,
        "total_time": total_time,
        "idle_time": idle_time
    }

def merge_gantt_segments(segments: List[GanttSegment]) -> List[GanttSegment]:
    """Merges adjacent Gantt segments of the same process to simplify the chart."""
    if not segments:
        return []
        
    merged = [GanttSegment(segments[0].pid, segments[0].start_time, segments[0].end_time)]
    
    for s in segments[1:]:
        last = merged[-1]
        if s.pid == last.pid and last.end_time == s.start_time:
            last.end_time = s.end_time
        else:
            merged.append(GanttSegment(s.pid, s.start_time, s.end_time))
            
    return merged
