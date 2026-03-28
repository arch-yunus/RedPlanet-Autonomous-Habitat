import argparse
from constants import *

def calculate_sabatier(co2_mass_kg, h2_mass_kg):
    """
    CO2 + 4H2 -> CH4 + 2H2O
    Stoichiometry: 1 mole CO2 : 4 moles H2
    """
    
    # Calculate moles
    moles_co2 = (co2_mass_kg * 1000) / MOLAR_MASS_CO2
    moles_h2_needed = moles_co2 * 4
    moles_h2_available = (h2_mass_kg * 1000) / MOLAR_MASS_H2
    
    # Determine limiting reagent
    if moles_h2_available < moles_h2_needed:
        actual_moles_co2_reacted = moles_h2_available / 4
        actual_moles_h2_reacted = moles_h2_available
        limiting = "Hydrogen"
    else:
        actual_moles_co2_reacted = moles_co2
        actual_moles_h2_reacted = moles_h2_needed
        limiting = "Carbon Dioxide"
        
    # Calculate products (with efficiency)
    moles_ch4_produced = actual_moles_co2_reacted * SABATIER_EFFICIENCY
    moles_h2o_produced = actual_moles_co2_reacted * 2 * SABATIER_EFFICIENCY
    
    # Convert back to mass (kg)
    ch4_kg = (moles_ch4_produced * MOLAR_MASS_CH4) / 1000
    h2o_kg = (moles_h2o_produced * MOLAR_MASS_H2O) / 1000
    
    return {
        "limiting_reagent": limiting,
        "methane_kg": round(ch4_kg, 3),
        "water_kg": round(h2o_kg, 3),
        "efficiency": SABATIER_EFFICIENCY
    }

def main():
    parser = argparse.ArgumentParser(description="Mars ISRU Sabatier Reactor Simulator")
    parser.add_argument("--co2", type=float, required=True, help="Intake CO2 mass in kg")
    parser.add_argument("--h2", type=float, required=True, help="Available H2 mass in kg")
    
    args = parser.parse_args()
    
    results = calculate_sabatier(args.co2, args.h2)
    
    print("-" * 40)
    print("?? Mars Sabatier Reactor Simulation Results")
    print("-" * 40)
    print(f"Input CO2: {args.co2} kg")
    print(f"Input H2:  {args.h2} kg")
    print(f"Limiting Reagent: {results['limiting_reagent']}")
    print("-" * 20)
    print(f"?? Methane (CH4) Produced: {results['methane_kg']} kg")
    print(f"?? Water (H2O) Produced:   {results['water_kg']} kg")
    print("-" * 40)

if __name__ == "__main__":
    main()
