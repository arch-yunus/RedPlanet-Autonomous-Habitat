import numpy as np
import matplotlib.pyplot as plt
from structure_grid import HabitatGrid
from rover_roles import RoverRole, RoleCapabilities

class SwarmRover:
    def __init__(self, start_pos, target_area, habitat_grid, role=RoverRole.CONSTRUCTOR):
        self.pos = np.array(start_pos, dtype=float)
        self.role = role
        self.stats = RoleCapabilities.get_stats(role)
        self.target_area = target_area
        self.target = self._generate_target()
        self.path = [self.pos.copy()]
        self.reached = False
        self.grid = habitat_grid
        self.cargo = 0
        
    def _generate_target(self):
        # Excavators go to resource zones, others to the building
        if self.role == RoverRole.EXCAVATOR:
            return np.array([np.random.uniform(0, 5), np.random.uniform(0, 5)])
        return np.array([
            np.random.uniform(self.target_area[0], self.target_area[1]),
            np.random.uniform(self.target_area[2], self.target_area[3])
        ])
        
    def step(self, neighbors=[]):
        if self.reached and self.role == RoverRole.CONSTRUCTOR:
            return
            
        speed = self.stats['speed']
        direction = self.target - self.pos
        dist = np.linalg.norm(direction)
        
        if dist < speed:
            self.pos = self.target.copy()
            if self.role == RoverRole.CONSTRUCTOR:
                self.reached = True
                self.grid.deposit(self.pos[0], self.pos[1])
            elif self.role == RoverRole.EXCAVATOR:
                self.cargo = self.stats['capacity']
                # Hand off logic simplified: go back and forth
                self.target = self.target_area[:2] # Head to construction
            elif self.role == RoverRole.TRANSPORTER:
                # Move between excavator and constructor
                pass
        else:
            move_vec = (direction / dist) * speed
            for other_pos in neighbors:
                repel_vec = self.pos - other_pos
                repel_dist = np.linalg.norm(repel_vec)
                if 0 < repel_dist < 1.2:
                    move_vec += (repel_vec / repel_dist) * (1.2 - repel_dist)
            self.pos += move_vec
            
        self.path.append(self.pos.copy())

def simulate_advanced_construction(num_rovers=20):
    habitat = HabitatGrid(size=(40, 40, 10))
    target_area = [15, 25, 15, 25]
    
    rovers = []
    for i in range(num_rovers):
        start = np.random.rand(2) * 10
        role = RoverRole.CONSTRUCTOR if i < 10 else (RoverRole.EXCAVATOR if i < 15 else RoverRole.TRANSPORTER)
        rovers.append(SwarmRover(start, target_area, habitat, role))
        
    for _ in range(300):
        positions = [r.pos for r in rovers]
        for i, r in enumerate(rovers):
            neighbors = [p for j, p in enumerate(positions) if i != j]
            r.step(neighbors=neighbors)
            
    return rovers, habitat
