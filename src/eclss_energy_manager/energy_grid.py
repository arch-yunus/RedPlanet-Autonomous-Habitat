import random

class EnergyGrid:
    def __init__(self, solar_capacity=100, nuclear_capacity=50):
        self.solar_capacity = solar_capacity
        self.nuclear_capacity = nuclear_capacity
        self.battery_level = 1000  # kWh
        self.battery_capacity = 2000
        
        # Load types and their consumption (kW)
        self.loads = {
            "Life Support": {"priority": 1, "consumption": 20, "active": True},
            "Communications": {"priority": 2, "consumption": 5, "active": True},
            "Habitat Lighting": {"priority": 3, "consumption": 10, "active": True},
            "ISRU Factory": {"priority": 4, "consumption": 150, "active": True},
            "Swarm Construction": {"priority": 5, "consumption": 80, "active": True}
        }
        
    def simulate_day(self, is_dust_storm=False):
        # Production
        solar_gen = self.solar_capacity * random.uniform(0.7, 1.0)
        if is_dust_storm:
            solar_gen *= random.uniform(0.05, 0.2)  # High attenuation
            
        nuclear_gen = self.nuclear_capacity
        total_gen = solar_gen + nuclear_gen
        
        # Consumption Management
        total_demand = sum(l["consumption"] for l in self.loads.values() if l["active"])
        
        # Smart load shedding if demand > generation and battery low
        if total_demand > total_gen and self.battery_level < 500:
            # Sort loads by priority (highest priority is 1)
            sorted_loads = sorted(self.loads.items(), key=lambda x: x[1]["priority"], reverse=True)
            for name, data in sorted_loads:
                if data["priority"] > 1: # Never shed life support
                    data["active"] = False
                    total_demand -= data["consumption"]
                    if total_demand <= total_gen:
                        break
        else:
            # Try to restore loads
            for name, data in self.loads.items():
                if not data["active"]:
                    if total_gen > total_demand + data["consumption"]:
                        data["active"] = True
                        total_demand += data["consumption"]

        # Battery update
        net_energy = total_gen - total_demand
        self.battery_level = max(0, min(self.battery_capacity, self.battery_level + net_energy))
        
        return {
            "generation": total_gen,
            "demand": total_demand,
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
