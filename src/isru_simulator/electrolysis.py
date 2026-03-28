from constants import *

def calculate_electrolysis(water_mass_kg):
    """
    2H2O -> 2H2 + O2
    Stoichiometry: 2 moles H2O : 2 moles H2 : 1 mole O2
    """
    moles_h2o = (water_mass_kg * 1000) / MOLAR_MASS_H2O
    
    # Electrolysis products
    moles_h2_produced = moles_h2o * ELECTROLYSIS_EFFICIENCY
    moles_o2_produced = (moles_h2o / 2) * ELECTROLYSIS_EFFICIENCY
    
    h2_kg = (moles_h2_produced * MOLAR_MASS_H2) / 1000
    o2_kg = (moles_o2_produced * MOLAR_MASS_O2) / 1000
    
    # Energy required: ~286 kJ/mol for standard, but let's assume 1.5x for Mars conditions
    energy_kwh = (moles_h2o * 286 * 1.5) / 3600 # kJ to kWh
    
    return {
        "h2_produced_kg": round(h2_kg, 3),
        "o2_produced_kg": round(o2_kg, 3),
        "energy_consumed_kwh": round(energy_kwh, 2)
    }
