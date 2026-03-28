class CrewMetabolism:
    def __init__(self, crew_size=6):
        self.crew_size = crew_size
        # Average daily needs per person (kg)
        self.o2_need_per_person = 0.84 # kg/day
        self.h2o_need_per_person = 3.0  # kg/day (drinking + food)
        self.co2_prod_per_person = 1.0  # kg/day
        
    def calculate_daily_requirements(self):
        return {
            "o2_kg": self.o2_need_per_person * self.crew_size,
            "h2o_kg": self.h2o_need_per_person * self.crew_size,
            "co2_kg": self.co2_prod_per_person * self.crew_size
        }
        
    def simulate_health_impact(self, o2_available_pct, h2o_available_pct):
        # returns health index (0 to 1)
        health = 1.0
        if o2_available_pct < 0.9:
            health -= (0.9 - o2_available_pct) * 2
        if h2o_available_pct < 0.8:
            health -= (0.8 - h2o_available_pct) * 0.5
        return max(0, health)
