import argparse
from constants import *
from electrolysis import calculate_electrolysis
from liquefaction import calculate_liquefaction
from compressor import calculate_compression_work
from heat_exchanger import calculate_heat_recovery
from metallurgy import extract_metals_from_regolith
from nitrogen_fixation import extract_n2_from_atmosphere, synthesize_ammonia

def calculate_full_isru_cycle(co2_mass_kg, water_mass_kg, regolith_mass_kg=0, air_intake_kg=0, energy_limit=10000):
    """
    1. Electrolysis: 2H2O -> 2H2 + O2
    2. Sabatier: CO2 + 4H2 -> CH4 + 2H2O
    3. Compression & Heat Recovery
    4. Metallurgy: Al & Fe extraction
    5. Nitrogen Fixation: N2 -> NH3 (v5.0)
    """
    
    # --- Phase 1: Electrolysis ---
    electrolysis_res = calculate_electrolysis(water_mass_kg)
    h2_available_kg = electrolysis_res['h2_produced_kg']
    o2_to_liquefy_kg = electrolysis_res['o2_produced_kg']
    
    # --- Phase 2: Sabatier Reactor ---
    moles_co2 = (co2_mass_kg * 1000) / MOLAR_MASS_CO2
    moles_h2_available = (h2_available_kg * 1000) / MOLAR_MASS_H2
    actual_moles_co2_reacted = min(moles_co2, moles_h2_available / 4)
    
    ch4_kg = (actual_moles_co2_reacted * SABATIER_EFFICIENCY * MOLAR_MASS_CH4) / 1000
    h2o_recovered_kg = (actual_moles_co2_reacted * 2 * SABATIER_EFFICIENCY * MOLAR_MASS_H2O) / 1000
    h2_consumed_kg = (actual_moles_co2_reacted * 4 * MOLAR_MASS_H2) / 1000
    
    # --- Phase 3: Advanced Engineering ---
    energy_comp = calculate_compression_work(co2_mass_kg, ATM_PRESSURE_MARS, 1000)
    energy_saved_heat = calculate_heat_recovery(actual_moles_co2_reacted, water_mass_kg)
    
    # --- Phase 4: Liquefaction ---
    energy_methane = calculate_liquefaction("CH4", ch4_kg)
    energy_oxygen = calculate_liquefaction("O2", o2_to_liquefy_kg)
    
    # --- Phase 5: Metallurgy ---
    energy_so_far = electrolysis_res['energy_consumed_kwh'] + energy_comp + energy_methane + energy_oxygen - energy_saved_heat
    metal_res = extract_metals_from_regolith(regolith_mass_kg, max(0, energy_limit - energy_so_far))
    
    # --- Phase 6: Nitrogen Fixation (v5.0) ---
    remaining_h2 = max(0, h2_available_kg - h2_consumed_kg)
    energy_after_metal = energy_so_far + metal_res['energy_consumed_kwh']
    
    n2_kg = extract_n2_from_atmosphere(air_intake_kg)
    nh3_res = synthesize_ammonia(n2_kg, remaining_h2, max(0, energy_limit - energy_after_metal))
    
    total_energy_kwh = energy_after_metal + nh3_res['energy_consumed_kwh']
    
    return {
        "methane_produced_kg": round(ch4_kg, 3),
        "water_recovered_kg": round(h2o_recovered_kg, 3),
        "oxygen_stored_kg": round(o2_to_liquefy_kg, 3),
        "iron_kg": metal_res['iron_kg'],
        "aluminum_kg": metal_res['aluminum_kg'],
        "ammonia_kg": nh3_res['ammonia_kg'],
        "total_energy_kwh": round(total_energy_kwh, 2),
        "electrolysis": electrolysis_res
    }

def main():
    parser = argparse.ArgumentParser(description="Mars ISRU Planetary Lifecycle Simulator")
    parser.add_argument("--co2", type=float, required=True)
    parser.add_argument("--water", type=float, required=True)
    parser.add_argument("--regolith", type=float, default=0)
    parser.add_argument("--air", type=float, default=0)
    
    args = parser.parse_args()
    res = calculate_full_isru_cycle(args.co2, args.water, args.regolith, args.air)
    
    print("-" * 50)
    print("?? RedPlanet ISRU v5.0: Planetary Scale Results")
    print("-" * 50)
    print(f"?? Methane: {res['methane_produced_kg']} kg | O2: {res['oxygen_stored_kg']} kg")
    print(f"?? Metals (Fe/Al): {res['iron_kg']}/{res['aluminum_kg']} kg")
    print(f"?? Ammonia (Fertilizer): {res['ammonia_kg']} kg")
    print(f"?? Total Energy: {res['total_energy_kwh']} kWh")
    print("-" * 50)

if __name__ == "__main__":
    main()
