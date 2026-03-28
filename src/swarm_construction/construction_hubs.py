class ConstructionHub:
    def __init__(self, location_id, radius_km=5.0):
        self.id = location_id
        self.radius = radius_km
        self.active_rovers = 0
        self.power_reserve_kwh = 10000.0
        
    def sync_swarm(self, rover_ids):
        self.active_rovers = len(rover_ids)
        # Hub provides 5% efficiency boost due to local low-latency relay
        return {
            "hub_id": self.id,
            "rovers_synced": self.active_rovers,
            "efficiency_multiplier": 1.05
        }
        
    def recharge_rover(self, rover_id, energy_needed):
        transfer = min(energy_needed, self.power_reserve_kwh * 0.05)
        self.power_reserve_kwh -= transfer
        return transfer
