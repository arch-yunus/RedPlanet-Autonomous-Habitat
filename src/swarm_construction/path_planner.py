import numpy as np
import matplotlib.pyplot as plt
from structure_grid import HabitatGrid

class SwarmRover:
    def __init__(self, start_pos, target_area, habitat_grid):
        self.pos = np.array(start_pos, dtype=float)
        # Target area is a range [x_min, x_max, y_min, y_max]
        self.target_area = target_area
        self.target = np.array([
            np.random.uniform(target_area[0], target_area[1]),
            np.random.uniform(target_area[2], target_area[3])
        ])
        self.path = [self.pos.copy()]
        self.reached = False
        self.grid = habitat_grid
        
    def step(self, speed=0.5, neighbors=[]):
        if self.reached:
            return
            
        direction = self.target - self.pos
        dist = np.linalg.norm(direction)
        
        if dist < speed:
            self.pos = self.target.copy()
            self.reached = True
            # Deposit regolit
            self.grid.deposit(self.pos[0], self.pos[1])
        else:
            move_vec = (direction / dist) * speed
            # Avoidance
            for other_pos in neighbors:
                repel_vec = self.pos - other_pos
                repel_dist = np.linalg.norm(repel_vec)
                if 0 < repel_dist < 1.5:
                    move_vec += (repel_vec / repel_dist) * (1.5 - repel_dist)
            
            self.pos += move_vec
            
        self.path.append(self.pos.copy())

def simulate_construction_phase(num_rovers=15):
    habitat = HabitatGrid(size=(30, 30, 5))
    target_area = [10, 20, 10, 20] # Center of the grid
    
    rovers = []
    for i in range(num_rovers):
        start = np.random.rand(2) * 5 # Start near origin
        rovers.append(SwarmRover(start, target_area, habitat))
        
    for _ in range(200):
        positions = [r.pos for r in rovers]
        for i, r in enumerate(rovers):
            neighbors = [p for j, p in enumerate(positions) if i != j]
            r.step(speed=0.6, neighbors=neighbors)
            
        if all(r.reached for r in rovers):
            break
            
    return rovers, habitat

def visualize_habitat(habitat):
    plt.figure(figsize=(8, 6))
    top_view = np.sum(habitat.grid, axis=2)
    plt.imshow(top_view, cmap='Oranges')
    plt.colorbar(label='Wall Height (Voxels)')
    plt.title("Mars Habitat Construction - 3D Print Progress (Top View)")
    plt.xlabel("X (Grid Units)")
    plt.ylabel("Y (Grid Units)")
    plt.savefig("habitat_progress.png")
    print("?? Construction progress saved as habitat_progress.png")

if __name__ == "__main__":
    print("?? Starting Advanced Swarm Construction...")
    rovers, habitat = simulate_construction_phase()
    print(f"?? Construction Progress: {habitat.get_progress():.4f}%")
    visualize_habitat(habitat)
