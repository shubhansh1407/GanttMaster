from core.models import Process

def get_basic_dataset():
    return [
        Process("P1", at=0, bt=5, priority=2),
        Process("P2", at=1, bt=3, priority=1),
        Process("P3", at=2, bt=8, priority=4),
        Process("P4", at=3, bt=6, priority=3),
    ]

def get_preemption_dataset():
    return [
        Process("P1", at=0, bt=8, priority=3),
        Process("P2", at=1, bt=4, priority=1),
        Process("P3", at=2, bt=2, priority=2),
        Process("P4", at=3, bt=1, priority=4),
    ]

def get_round_robin_dataset():
    return [
        Process("P1", at=0, bt=5, priority=1),
        Process("P2", at=1, bt=4, priority=2),
        Process("P3", at=2, bt=2, priority=3),
        Process("P4", at=3, bt=1, priority=4),
    ]

DATASETS = {
    "Basic": get_basic_dataset,
    "Preemption (SRTF)": get_preemption_dataset,
    "Round Robin": get_round_robin_dataset
}
