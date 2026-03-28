from constants import *

def extract_metals_from_regolith(regolith_mass_kg, energy_available_kwh):
    """
    Molten Salt Electrolysis (MSE) model.
    Yields Al and Fe from regolith oxides (Al2O3, Fe2O3).
    Average yield: ~15% Fe, ~7% Al by mass.
    Energy density: ~15-20 kWh per kg of metal.
    """
    
    ENERGY_PER_KG_METAL = 18.0 # kWh/kg
    max_metal_possible_kg = energy_available_kwh / ENERGY_PER_KG_METAL
    
    # Check regolith physical limit
    theoretical_fe = regolith_mass_kg * 0.15
    theoretical_al = regolith_mass_kg * 0.07
    total_theoretical = theoretical_fe + theoretical_al
    
    actual_metal_total = min(total_theoretical, max_metal_possible_kg)
    
    # Proportional distribution
    yield_fe = actual_metal_total * (0.15 / 0.22)
    yield_al = actual_metal_total * (0.07 / 0.22)
    
    return {
        "iron_kg": round(yield_fe, 3),
        "aluminum_kg": round(yield_al, 3),
        "energy_consumed_kwh": round(actual_metal_total * ENERGY_PER_KG_METAL, 2)
    }
