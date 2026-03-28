import math

def calculate_orbital_refueling(propellant_mass_kg, orbit_altitude_km=500):
    """
    Model propellant transfer to an orbital depot.
    Includes boil-off rate and transfer efficiency.
    """
    BOIL_OFF_RATE_PER_DAY = 0.001 # 0.1% loss per day
    TRANSFER_EFFICIENCY = 0.98
    
    # Delta V for Mars surface to LEO-like orbit: ~4.1 km/s
    # Simplified mass fraction
    delivered_mass = propellant_mass_kg * TRANSFER_EFFICIENCY
    
    return {
        "delivered_propellant_kg": round(delivered_mass, 2),
        "daily_boil_off_kg": round(delivered_mass * BOIL_OFF_RATE_PER_DAY, 4),
        "transfer_efficiency": TRANSFER_EFFICIENCY
    }
