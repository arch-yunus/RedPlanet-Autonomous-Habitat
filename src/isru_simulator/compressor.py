import math
from constants import *

def calculate_compression_work(mass_kg, p_in_hpa, p_out_hpa, stages=3):
    """
    Isentropic compression work for multi-stage system with intercooling.
    W_dot = (n * P_in * V_dot / (eta_is * (n-1))) * [(P_out/P_in)^((n-1)/n) - 1]
    Simplified per kg: w = (stages * R * T_in / (eta_is * (gamma-1)/gamma)) * [(P_out/P_in)^((gamma-1)/(gamma*stages)) - 1]
    """
    
    GAMMA = 1.3  # For large molecules like CO2/CH4
    R_SPECIFIC = 0.1889 # kJ/(kg*K) for CO2
    T_IN = 273 + AVERAGE_TEMP_MARS # Kelvin
    ETA_IS = 0.75 # Isentropic efficiency
    
    pressure_ratio = p_out_hpa / p_in_hpa
    exponent = (GAMMA - 1) / (GAMMA * stages)
    
    # Work in kJ/kg
    work_per_kg = (stages * R_SPECIFIC * T_IN / (ETA_IS * (GAMMA - 1) / GAMMA)) * (math.pow(pressure_ratio, exponent) - 1)
    
    total_work_kj = mass_kg * work_per_kg
    # Convert to kWh
    return round(total_work_kj / 3600, 3)
