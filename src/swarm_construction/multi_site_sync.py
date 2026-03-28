import numpy as np

class SiteCoordinator:
    def __init__(self, sites):
        """
        sites: dict of {name: bounds}
        """
        self.sites = sites
        self.assignments = {} # rover_id: site_name
        
    def assign_rover(self, rover_id, site_name):
        if site_name in self.sites:
            self.assignments[rover_id] = site_name
            return self.sites[site_name]
        return None
        
    def get_site_bounds(self, site_name):
        return self.sites.get(site_name)
