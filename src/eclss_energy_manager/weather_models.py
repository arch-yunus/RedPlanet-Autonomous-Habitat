import numpy as np

def get_solar_flux(ls_deg):
    """
    Calculate solar flux on Mars based on Solar Longitude (Ls)
    Ls: 0 (Spring Equinox), 90 (Summer Solstice), 180 (Autumn Equinox), 270 (Winter Solstice)
    """
    # Mars-Sun distance varies: r = a(1-e^2)/(1+e*cos(theta))
    # Simplified flux model: Flux = Flux_avg * (d_avg / d)^2
    
    # Average solar constant at Mars orbital distance
    SOLAR_CONSTANT_MARS = 588.6 # W/m^2
    
    # Orbital eccentricity of Mars is high (0.0934)
    e = 0.0934
    # Peak flux is at Perihelion (near Ls=250), Min at Aphelion (near Ls=70)
    # theta is true anomaly, related to Ls
    theta = np.radians(ls_deg - 250)
    
    relative_dist_sq = ((1 + e * np.cos(theta)) / (1 - e**2))**2
    flux = SOLAR_CONSTANT_MARS * relative_dist_sq
    
    return round(flux, 2)

def simulate_ls_cycle(days_since_start):
    # One Mars Year is approx 668.6 Sols
    # Each Sol is approx 1/668.6 of the orbit
    ls_deg = (days_since_start / 668.6) * 360 % 360
    return ls_deg
