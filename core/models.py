from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Process:
    pid: str
    at: int  # Arrival Time
    bt: int  # Burst Time
    priority: int = 0

@dataclass
class ProcessMetrics:
    pid: str
    at: int
    bt: int
    priority: int
    ct: int  # Completion Time
    tat: int # Turnaround Time
    wt: int  # Waiting Time
    rt: int  # Response Time

@dataclass
class GanttSegment:
    pid: str
    start_time: int
    end_time: int
    
    @property
    def duration(self):
        return self.end_time - self.start_time

@dataclass
class SimulationResult:
    processes: List[ProcessMetrics]
    gantt: List[GanttSegment]
    avg_wt: float
    avg_tat: float
    avg_rt: float
    cpu_utilization: float
    throughput: float
    total_time: int
    idle_time: int
