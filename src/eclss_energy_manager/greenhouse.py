class HydroponicGreenhouse:
    def __init__(self, area_m2=50):
        self.area = area_m2
        self.biomass_kg = 10.0
        # 1 m2 of plants can produce ~50-100g of O2 per day
        self.o2_prod_per_m2 = 0.08 # kg/day
        self.h2o_consumption_per_m2 = 2.0 # kg/day
        
    def simulate_day(self, energy_available_kwh):
        # Greenhouses need lighting energy: ~1 kWh/m2/day
        efficiency = min(1.0, energy_available_kwh / self.area)
        
        o2_yield = self.area * self.o2_prod_per_m2 * efficiency
        h2o_needed = self.area * self.h2o_consumption_per_m2 * efficiency
        
        self.biomass_kg += (o2_yield * 0.5) # simplified growth
        
        return {
            "o2_produced_kg": round(o2_yield, 3),
            "h2o_consumed_kg": round(h2o_needed, 3),
            "energy_consumed_kwh": round(self.area * efficiency, 2),
            "food_yield_kg": round(self.biomass_kg * 0.01, 3) # 1% harvestable
        }
