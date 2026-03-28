import numpy as np
import matplotlib.pyplot as plt

class SwarmRover:
    def __init__(self, start_pos, target_pos):
        self.pos = np.array(start_pos, dtype=float)
        self.target = np.array(target_pos, dtype=float)
        self.path = [self.pos.copy()]
        self.reached = False
        
    def step(self, speed=0.5, neighbors=[]):
        if self.reached:
            return
            
        # Basic vector to target
        direction = self.target - self.pos
        dist = np.linalg.norm(direction)
        
        if dist < speed:
            self.pos = self.target.copy()
            self.reached = True
        else:
            # Normalize and move
            move_vec = (direction / dist) * speed
            
            # Simple collision avoidance with neighbors
            for other_pos in neighbors:
                repel_vec = self.pos - other_pos
                repel_dist = np.linalg.norm(repel_vec)
                if 0 < repel_dist < 2.0:
                    move_vec += (repel_vec / repel_dist) * (2.0 - repel_dist)
            
            self.pos += move_vec
            
        self.path.append(self.pos.copy())

def simulate_swarm(num_rovers=10, target=[20, 20]):
    rovers = []
    for i in range(num_rovers):
        start = np.random.rand(2) * 10
        rovers.append(SwarmRover(start, target))
        
    for _ in range(100):
        positions = [r.pos for r in rovers]
        for i, r in enumerate(rovers):
            neighbors = [p for j, p in enumerate(positions) if i != j]
            r.step(speed=0.5, neighbors=neighbors)
            
        if all(r.reached for r in rovers):
            break
            
    return rovers

def visualize_paths(rovers):
    plt.figure(figsize=(10, 8))
    for r in rovers:
        path = np.array(r.path)
        plt.plot(path[:, 0], path[:, 1], alpha=0.6)
        plt.scatter(path[-1, 0], path[-1, 1], marker='o')
        
    plt.title("Mars Swarm Construction - Rover Pathfinding")
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.grid(True)
    plt.savefig("swarm_paths.png")
    print("?? Swarm path visualization saved as swarm_paths.png")

if __name__ == "__main__":
    print("?? Starting Mars Swarm Intelligence Simulation...")
    rovers = simulate_swarm()
    visualize_paths(rovers)
