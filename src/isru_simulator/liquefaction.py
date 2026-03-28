from constants import *

def calculate_liquefaction(gas_type, mass_kg):
    """
    Calculate energy needed to liquefy gases (CH4 or O2)
    Simplified model: E = m * CP * deltaT + m * HeatOfVaporization
    """
    
    # Constants (approximate)
    if gas_type == "CH4":
        cp = 2.2  # kJ/(kg*K)
        target_temp = 111 # Kelvin (Liquid methane boiling point)
        latent_heat = 510 # kJ/kg
    elif gas_type == "O2":
        cp = 0.918
        target_temp = 90 # Kelvin
        latent_heat = 213
    else:
        return 0
        
    delta_t = (273 + AVERAGE_TEMP_MARS) - target_temp
    
    # Cooling Energy
    q_sensible = mass_kg * cp * max(0, delta_t)
    # Phase Change Energy
    q_latent = mass_kg * latent_heat
    
    total_energy_kj = q_sensible + q_latent
    # Actual cooling work is higher (Carnot efficiency + losses)
    actual_work_kwh = (total_energy_kj * 2.5) / 3600 
    
    return round(actual_work_kwh, 2)
