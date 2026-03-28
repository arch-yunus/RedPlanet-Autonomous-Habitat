import random
from weather_models import get_solar_flux, simulate_ls_cycle
from human_metabolism import CrewMetabolism
from greenhouse import HydroponicGreenhouse
from psychology import CrewPsychology
from radiation_model import RadiationModel
from health_ai import HealthAIPredictor
from quantum_governor import QuantumGovernor

class EnergyGrid:
    def __init__(self, solar_capacity_coeff=0.2, nuclear_capacity=60, crew_size=6):
        self.solar_coeff = solar_capacity_coeff 
        self.nuclear_capacity = nuclear_capacity
        self.battery_level = 1000 
        self.battery_capacity = 2000
        self.battery_health = 1.0
        self.days_elapsed = 0
        
        self.crew = CrewMetabolism(crew_size)
        self.greenhouse = HydroponicGreenhouse(50)
        self.psychology = CrewPsychology(crew_size)
        self.radiation = RadiationModel()
        self.health_ai = HealthAIPredictor(self.crew)
        self.governor = QuantumGovernor(self)
        
        self.habitat_o2 = 500  # kg reserve
        self.habitat_h2o = 2000 # kg reserve
        self.crew_health = 1.0
        
        self.loads = {
            "Life Support": {"priority": 1, "consumption": 30, "active": True},
            "Communications": {"priority": 2, "consumption": 5, "active": True},
            "Habitat Lighting": {"priority": 3, "consumption": 10, "active": True},
            "ISRU Factory": {"priority": 4, "consumption": 200, "active": True},
            "Swarm Construction": {"priority": 5, "consumption": 80, "active": True}
        }
        
    def simulate_day(self, is_dust_storm=False, isru_o2_prod=0, isru_h2o_prod=0):
        self.days_elapsed += 1
        ls = simulate_ls_cycle(self.days_elapsed)
        available_flux = get_solar_flux(ls)
        
        # Power Production
        solar_gen = self.solar_coeff * available_flux * random.uniform(0.85, 1.0)
        if is_dust_storm:
            solar_gen *= random.uniform(0.01, 0.12)
            
        nuclear_gen = self.nuclear_capacity
        total_gen = solar_gen + nuclear_gen
        
        # Consumption
        total_demand = sum(l["consumption"] for l in self.loads.values() if l["active"])
        
        # Load Shedding
        eff_cap = self.battery_capacity * self.battery_health
        if total_demand > total_gen and self.battery_level < (eff_cap * 0.25):
            for name, data in sorted(self.loads.items(), key=lambda x: x[1]["priority"], reverse=True):
                if data["priority"] > 1:
                    data["active"] = False
                    total_demand -= data["consumption"]
                    if total_demand <= total_gen: break
        else:
            for name, data in self.loads.items():
                if not data["active"] and total_gen > total_demand + data["consumption"]:
                    data["active"] = True
                    total_demand += data["consumption"]

        # Resource turnover
        needs = self.crew.calculate_daily_requirements()
        o2_supplied = min(self.habitat_o2 + isru_o2_prod, needs['o2_kg'])
        h2o_supplied = min(self.habitat_h2o + isru_h2o_prod, needs['h2o_kg'])
        
        self.habitat_o2 = max(0, self.habitat_o2 + isru_o2_prod - needs['o2_kg'])
        self.habitat_h2o = max(0, self.habitat_h2o + isru_h2o_prod - needs['h2o_kg'])
        
        self.crew_health = self.crew.simulate_health_impact(
            o2_supplied / needs['o2_kg'],
            h2o_supplied / needs['h2o_kg']
        )

        net_energy = total_gen - total_demand
        self.battery_level = max(0, min(eff_cap, self.battery_level + net_energy))
        self.battery_health -= 0.00004
        
        return {
            "ls": ls,
            "generation": total_gen,
            "demand": total_demand,
            "crew_health": self.crew_health,
            "o2_reserve": self.habitat_o2,
            "h2o_reserve": self.habitat_h2o,
            "battery": self.battery_level,
            "shed_count": sum(1 for l in self.loads.values() if not l["active"])
        }

if __name__ == "__main__":
    grid = EnergyGrid()
    print("?? Starting 7-day Mars Energy Simulation (3 days of Dust Storm)")
    print("-" * 30)
    for day in range(1, 8):
        storm = 3 <= day <= 5
        res = grid.simulate_day(storm)
        storm_str = "?? STORM" if storm else "?? CLEAR"
        print(f"Day {day} | {storm_str} | Gen: {res['generation']:.1f}kW | Bat: {res['battery']:.1f}kWh | Shed: {res['shed_count']}")
