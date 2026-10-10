from algorithms import fcfs, sjf, srtf, priority, round_robin

ALGORITHMS = {
    "FCFS": fcfs.simulate,
    "SJF": sjf.simulate,
    "SRTF": srtf.simulate,
    "Priority": priority.simulate,
    "Round Robin": round_robin.simulate
}
