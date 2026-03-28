class PlanetaryBiosphere:
    def __init__(self, initial_temp_k=210, initial_pressure_hpa=6.1):
        self.surface_temp_k = initial_temp_k
        self.atm_pressure_hpa = initial_pressure_hpa
        self.years_elapsed = 0
        self.viable_land_pct = 0.0 # 0 to 100
        
    def simulate_year(self, pfc_mass_added_kg, solar_mirror_focus=0):
        self.years_elapsed += 1
        
        # Warming: 1 GT PFC ~ 0.25 K
        warming = (pfc_mass_added_kg / 1e12) * 0.25
        self.surface_temp_k += warming
        
        # Pressure increase due to sublimation of CO2 ice caps at poles
        if self.surface_temp_k > 220:
            pressure_boost = (self.surface_temp_k - 220) * 0.5
            self.atm_pressure_hpa += pressure_boost
            
        # Habitability index
        if self.surface_temp_k > 273 and self.atm_pressure_hpa > 600:
            self.viable_land_pct = min(100.0, self.viable_land_pct + 1.0)
            
        return {
            "year": self.years_elapsed,
            "temp_k": round(self.surface_temp_k, 2),
            "pressure_hpa": round(self.atm_pressure_hpa, 1),
            "habitability_pct": round(self.viable_land_pct, 2)
        }
