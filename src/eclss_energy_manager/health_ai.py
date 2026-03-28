class HealthAIPredictor:
    def __init__(self, crew_metabolism):
        self.crew = crew_metabolism
        self.history = []
        
    def diagnose(self, current_health):
        self.history.append(current_health)
        if len(self.history) > 24: self.history.pop(0)
        
        trend = self.history[-1] - self.history[0] if len(self.history) > 1 else 0
        
        status = "NOMINAL"
        recommendation = "Maintain current levels."
        
        if current_health < 80 or trend < -0.1:
            status = "WARNING: Health degradation detected."
            recommendation = "Increase O2 buffer and nutrient density."
            
        return {
            "status": status,
            "trend": round(trend, 4),
            "recommendation": recommendation
        }
