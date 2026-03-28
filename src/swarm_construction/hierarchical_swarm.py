from rover_roles import RoverRole

class SwarmHierarchy:
    def __init__(self, rovers):
        self.rovers = rovers # list of rover objects
        self.leader = None
        
    def designate_leader(self):
        # Scout with best batteries becomes leader
        scouts = [r for r in self.rovers if r.role == RoverRole.EXCAVATOR] # using excavator as proxy for scout
        if scouts:
            self.leader = max(scouts, key=lambda r: r.stats['power'])
            return self.leader
        return None
        
    def broadcast_command(self, target_pos):
        if self.leader:
            for r in self.rovers:
                if r != self.leader:
                    r.target = target_pos + (np.random.rand(2) * 2)
