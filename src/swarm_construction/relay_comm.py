import math

def calculate_signal_loss(distance_km, frequency_ghz=2.4):
    """
    Free-space path loss (FSPL).
    FSPL (dB) = 20log10(d) + 20log10(f) + 92.45
    """
    if distance_km <= 0: return 0
    return 20 * math.log10(distance_km) + 20 * math.log10(frequency_ghz) + 92.45

def get_latency_ms(distance_km):
    # Speed of light ~300,000 km/s
    return (distance_km / 300000.0) * 1000.0
