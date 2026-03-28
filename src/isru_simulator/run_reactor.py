import argparse
from constants import *
from electrolysis import calculate_electrolysis
from liquefaction import calculate_liquefaction

def calculate_full_isru_cycle(co2_mass_kg, water_mass_kg):
    """
    1. Electrolysis: 2H2O -> 2H2 + O2
    2. Sabatier: CO2 + 4H2 -> CH4 + 2H2O
    3. Liquefaction: Cool results to storage temps
    """
    
    # --- Phase 1: Electrolysis ---
    electrolysis_res = calculate_electrolysis(water_mass_kg)
    h2_available_kg = electrolysis_res['h2_produced_kg']
    o2_to_liquefy_kg = electrolysis_res['o2_produced_kg']
    
    # --- Phase 2: Sabatier Reactor ---
    moles_co2 = (co2_mass_kg * 1000) / MOLAR_MASS_CO2
    moles_h2_needed = moles_co2 * 4
    moles_h2_available = (h2_available_kg * 1000) / MOLAR_MASS_H2
    
    actual_moles_co2_reacted = min(moles_co2, moles_h2_available / 4)
    
    moles_ch4_produced = actual_moles_co2_reacted * SABATIER_EFFICIENCY
    moles_h2o_produced = actual_moles_co2_reacted * 2 * SABATIER_EFFICIENCY
    
    ch4_kg = (moles_ch4_produced * MOLAR_MASS_CH4) / 1000
    h2o_recovered_kg = (moles_h2o_produced * MOLAR_MASS_H2O) / 1000
    
    # --- Phase 3: Liquefaction ---
    energy_methane = calculate_liquefaction("CH4", ch4_kg)
    energy_oxygen = calculate_liquefaction("O2", o2_to_liquefy_kg)
    
    total_energy_kwh = (
        electrolysis_res['energy_consumed_kwh'] + 
        energy_methane + 
        energy_oxygen
    )
    
    return {
        "methane_produced_kg": round(ch4_kg, 3),
        "water_recovered_kg": round(h2o_recovered_kg, 3),
        "oxygen_stored_kg": round(o2_to_liquefy_kg, 3),
        "total_energy_kwh": round(total_energy_kwh, 2),
        "electrolysis": electrolysis_res
    }

def main():
    parser = argparse.ArgumentParser(description="Mars ISRU Full Lifecycle Simulator")
    parser.add_argument("--co2", type=float, required=True, help="Intake CO2 mass in kg")
    parser.add_argument("--water", type=float, required=True, help="Intake Water mass in kg")
    
    args = parser.parse_args()
    
    results = calculate_full_isru_cycle(args.co2, args.water)
    
    print("-" * 50)
    print("?? RedPlanet ISRU: Full Chemical Cycle Results")
    print("-" * 50)
    print(f"?? Electrolysis Input: {args.water} kg H2O")
    print(f"?? H2 Produced for Sabatier: {results['electrolysis']['h2_produced_kg']} kg")
    print(f"?? O2 Produced for Storage:  {results['oxygen_stored_kg']} kg")
    print("-" * 25)
    print(f"?? Methane (CH4) Output: {results['methane_produced_kg']} kg")
    print(f"?? Recovered Water:      {results['water_recovered_kg']} kg")
    print("-" * 25)
    print(f"?? Total Energy Consumed: {results['total_energy_kwh']} kWh")
    print("-" * 50)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
