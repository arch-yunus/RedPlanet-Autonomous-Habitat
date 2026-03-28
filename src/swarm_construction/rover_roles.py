from enum import Enum

class RoverRole(Enum):
    EXCAVATOR = "Excavator"    # Gathers regolit from surface
    TRANSPORTER = "Transporter" # Moves regolit to construction site
    CONSTRUCTOR = "Constructor" # 3D prints the habitat shell

class RoleCapabilities:
    @staticmethod
    def get_stats(role):
        if role == RoverRole.EXCAVATOR:
            return {"speed": 0.4, "capacity": 50, "power": 15}
        elif role == RoverRole.TRANSPORTER:
            return {"speed": 0.8, "capacity": 100, "power": 10}
        elif role == RoverRole.CONSTRUCTOR:
            return {"speed": 0.3, "capacity": 20, "power": 25}
        return {"speed": 0.5, "capacity": 0, "power": 5}
