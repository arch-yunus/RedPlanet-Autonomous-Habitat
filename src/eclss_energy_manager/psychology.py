class CrewPsychology:
    def __init__(self, crew_size=6):
        self.stress_levels = [0.1] * crew_size # 0 nominal, 1 breakdown
        
    def update_stress(self, resource_availability, is_storm):
        # resource_availability: 0 to 1
        for i in range(len(self.stress_levels)):
            delta = 0.01
            if resource_availability < 0.8:
                delta += 0.05
            if is_storm:
                delta += 0.03
            else:
                delta -= 0.02
                
            self.stress_levels[i] = max(0, min(1, self.stress_levels[i] + delta))
            
    def get_mission_effectiveness(self):
        avg_stress = sum(self.stress_levels) / len(self.stress_levels)
        return round(1.0 - (avg_stress * 0.5), 2)
