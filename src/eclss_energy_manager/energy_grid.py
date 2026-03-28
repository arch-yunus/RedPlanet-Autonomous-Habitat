import random
from weather_models import get_solar_flux, simulate_ls_cycle

class EnergyGrid:
    def __init__(self, solar_capacity_coeff=0.2, nuclear_capacity=60):
        # solar_capacity_coeff is conversion efficiency * surface area
        self.solar_coeff = solar_capacity_coeff 
        self.nuclear_capacity = nuclear_capacity
        self.battery_level = 1000 
        self.battery_capacity = 2000
        self.battery_health = 1.0 # 100% health
        self.days_elapsed = 0
        
        self.loads = {
            "Life Support": {"priority": 1, "consumption": 25, "active": True},
            "Communications": {"priority": 2, "consumption": 5, "active": True},
            "Habitat Lighting": {"priority": 3, "consumption": 8, "active": True},
            "ISRU Factory": {"priority": 4, "consumption": 180, "active": True},
            "Swarm Construction": {"priority": 5, "consumption": 60, "active": True}
        }
        
    def simulate_day(self, is_dust_storm=False):
        self.days_elapsed += 1
        ls = simulate_ls_cycle(self.days_elapsed)
        available_flux = get_solar_flux(ls)
        
        # Production
        solar_gen = self.solar_coeff * available_flux * random.uniform(0.85, 1.0)
        if is_dust_storm:
            solar_gen *= random.uniform(0.02, 0.15)
            
        nuclear_gen = self.nuclear_capacity
        total_gen = solar_gen + nuclear_gen
        
        # Degradation: Battery health drops slightly every cycle
        self.battery_health -= 0.00005 # ~1.8% per year
        eff_battery_capacity = self.battery_capacity * self.battery_health
        
        # Consumption Management
        total_demand = sum(l["consumption"] for l in self.loads.values() if l["active"])
        
        if total_demand > total_gen and self.battery_level < (eff_battery_capacity * 0.3):
            sorted_loads = sorted(self.loads.items(), key=lambda x: x[1]["priority"], reverse=True)
            for name, data in sorted_loads:
                if data["priority"] > 1:
                    data["active"] = False
                    total_demand -= data["consumption"]
                    if total_demand <= total_gen:
                        break
        else:
            for name, data in self.loads.items():
                if not data["active"]:
                    if total_gen > total_demand + data["consumption"]:
                        data["active"] = True
                        total_demand += data["consumption"]

        net_energy = total_gen - total_demand
        self.battery_level = max(0, min(eff_battery_capacity, self.battery_level + net_energy))
        
        return {
            "ls": ls,
            "flux": available_flux,
            "generation": total_gen,
            "demand": total_demand,
            "battery": self.battery_level,
            "battery_health": self.battery_health,
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
