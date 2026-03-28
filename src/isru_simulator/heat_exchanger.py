from constants import *

def calculate_heat_recovery(reaction_moles, target_water_kg):
    """
    Sabatier is exothermic: deltaH ~ -165 kJ/mol
    We recover this heat to pre-heat electrolysis water.
    """
    
    HEAT_OF_REACTION = 165 # kJ/mol
    total_heat_available_kj = reaction_moles * HEAT_OF_REACTION * 0.6 # 60% recovery efficiency
    
    # Energy to heat water from -60C to 20C
    # Q = m * cp * deltaT
    cp_water = 4.18 # kJ/(kg*K)
    delta_t = 80 # -60 to 20
    heat_needed_kj = target_water_kg * cp_water * delta_t
    
    recovered_kj = min(total_heat_available_kj, heat_needed_kj)
    # Energy saved in kWh
    return round(recovered_kj / 3600, 3)
