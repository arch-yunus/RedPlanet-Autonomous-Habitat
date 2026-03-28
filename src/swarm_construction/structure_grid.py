import numpy as np

class HabitatGrid:
    def __init__(self, size=(20, 20, 10)):
        self.grid = np.zeros(size, dtype=int)
        self.width, self.depth, self.height = size
        
    def deposit(self, x, y):
        # Find the first empty z level at (x, y)
        ix, iy = int(x), int(y)
        if 0 <= ix < self.width and 0 <= iy < self.depth:
            for z in range(self.height):
                if self.grid[ix, iy, z] == 0:
                    self.grid[ix, iy, z] = 1
                    return True
        return False
        
    def get_progress(self):
        total_voxels = self.grid.size
        built_voxels = np.sum(self.grid)
        return (built_voxels / total_voxels) * 100
