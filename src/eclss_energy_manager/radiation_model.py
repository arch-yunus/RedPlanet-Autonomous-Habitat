import random

class RadiationModel:
    def __init__(self):
        self.cumulative_dose_msv = 0.0
        self.gcr_base_rate = 0.5 / 24.0 # mSv/hour
        
    def simulate_hour(self, is_solar_storm=False):
        dose = self.gcr_base_rate
        if is_solar_storm:
            dose += random.uniform(5.0, 50.0) # SPE event
            
        self.cumulative_dose_msv += dose
        # Hardware degradation: solar panel efficiency loss
        hardware_deg = 1.0 - (self.cumulative_dose_msv * 0.000001)
        
        return {
            "dose_hourly_msv": round(dose, 4),
            "total_dose_msv": round(self.cumulative_dose_msv, 2),
            "hardware_health": round(hardware_deg, 6)
        }
