import math

def calculate_pfc_effect(mass_pfc_kg):
    """
    Simplified model for the greenhouse effect of PFCs on Mars.
    1 kg of CF4/C2F6 is ~10,000x more potent than CO2.
    """
    # Radiative forcing of PFCs: ~0.1 - 0.5 W/m2 per gigaton
    forcing_w_m2 = (mass_pfc_kg / 1e12) * 0.25
    
    # Delta T = lambda * delta F (lambda ~ 0.25 K / (W/m2) for Mars)
    delta_t = 0.25 * forcing_w_m2
    
    return {
        "forcing_w_m2": round(forcing_w_m2, 6),
        "temperature_increase_k": round(delta_t, 4),
        "warming_coefficient": 10000 # potency vs CO2
    }

def optimize_warming_yield(current_isru_byproducts):
    """
    Adjust ISRU parameters to maximize fluorine-based gas output for warming.
    """
    # (Conceptual logic for redirection of reactant streams)
    return {
        "isru_mode": "WARMING_GENESIS",
        "pfc_byproduct_kg_per_sol": random.uniform(0.1, 0.5)
    }
