from enum import Enum
import random

class RepairStatus(Enum):
    NOMINAL = 0
    DEGRADED = 1
    FAILED = 2

def simulate_component_damage(component_name, chance=0.01):
    if random.random() < chance:
        return RepairStatus.DEGRADED
    return RepairStatus.NOMINAL

def perform_repair(component_status):
    if component_status == RepairStatus.DEGRADED:
        return RepairStatus.NOMINAL, 5.0 # costs energy
    return component_status, 0.0
