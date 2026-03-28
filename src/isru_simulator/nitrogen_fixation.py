from constants import *

def synthesize_ammonia(n2_mass_kg, h2_mass_kg, energy_available_kwh):
    """
    Haber-Bosch simplified model for Mars conditions.
    N2 + 3H2 -> 2NH3
    Requires high pressure and catalyst.
    """
    
    # Stoichiometry
    moles_n2 = (n2_mass_kg * 1000) / 28.01
    moles_h2 = (h2_mass_kg * 1000) / 2.016
    
    actual_moles_n2 = min(moles_n2, moles_h2 / 3.0)
    
    # Haber-Bosch energy: ~1-2 kWh per kg of NH3 produced
    ENERGY_PER_KG_NH3 = 1.6 # kWh/kg
    max_nh3_from_energy = energy_available_kwh / ENERGY_PER_KG_NH3
    
    theoretical_nh3_kg = (actual_moles_n2 * 2 * 17.031) / 1000
    actual_nh3_kg = min(theoretical_nh3_kg, max_nh3_from_energy)
    
    # Consumed Hydrogen
    h2_used_kg = (actual_nh3_kg * 3 * 2.016) / (2 * 17.031)
    
    return {
        "ammonia_kg": round(actual_nh3_kg, 3),
        "h2_used_kg": round(h2_used_kg, 3),
        "energy_consumed_kwh": round(actual_nh3_kg * ENERGY_PER_KG_NH3, 2)
    }

def extract_n2_from_atmosphere(intake_air_kg):
    """
    Mars atmosphere is ~2.7% N2.
    """
    return round(intake_air_kg * 0.027, 4)
