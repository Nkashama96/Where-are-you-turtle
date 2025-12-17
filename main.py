import random
import math
import time

# ===============================
# Utility functions
# ===============================

def format_years(years: int) -> str:
    """Format years with comma separators."""
    return f"{years:,}"

def clamp_lat(lat: float) -> float:
    """Clamp latitude between South and North Pole."""
    return max(-90.0, min(90.0, lat))

def wrap_lon(lon: float) -> float:
    """Wrap longitude to [-180, 180]."""
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360
    return lon

def distance_deg(lat1, lon1, lat2, lon2) -> float:
    """
    Approx distance in degrees (simplified spherical distance).
    Good enough for a philosophical simulation.
    """
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


# ===============================
# Turtle
# ===============================

class Turtle:
    """
    Sea turtle with realistic movement scale.
    Speed reference:
      ~3 km/h average cruising
      ~26,000 km / year max (used as directional drift)
    """
    def __init__(self):
        self.lat = random.uniform(-60, 60)
        self.lon = random.uniform(-180, 180)

    def move(self):
        # Random heading
        angle = random.uniform(0, 2 * math.pi)

        # Convert km/year roughly into degrees/year
        # 1 degree latitude ≈ 111 km
        speed_km_per_year = random.uniform(1000, 3000)
        delta_deg = speed_km_per_year / 111_000

        self.lat += math.sin(angle) * delta_deg
        self.lon += math.cos(angle) * delta_deg

        self.lat = clamp_lat(self.lat)
        self.lon = wrap_lon(self.lon)


# ===============================
# Yoke
# ===============================

class Yoke:
    """
    Floating yoke affected by:
      - Ocean currents
      - Wind
      - Seasonal oscillation
    Speed reference:
      ~0.1–1 m/s (ocean currents)
    """
    def __init__(self):
        self.lat = random.uniform(-60, 60)
        self.lon = random.uniform(-180, 180)
        self.season_phase = random.uniform(0, 2 * math.pi)

    def move(self, year):
        # Seasonal oscillation (slow sine wave)
        seasonal_drift = 0.01 * math.sin(self.season_phase + year / 50)

        # Ocean current drift (very slow)
        current_lat = random.uniform(-0.005, 0.005)
        current_lon = random.uniform(-0.01, 0.01)

        # Wind noise
        wind_lat = random.uniform(-0.002, 0.002)
        wind_lon = random.uniform(-0.002, 0.002)

        self.lat += current_lat + wind_lat + seasonal_drift
        self.lon += current_lon + wind_lon

        self.lat = clamp_lat(self.lat)
        self.lon = wrap_lon(self.lon)


# ===============================
# Simulation
# ===============================

def simulate():
    turtle = Turtle()
    yoke = Yoke()

    YEARS_PER_BREATH = 100
    SUCCESS_RADIUS = 0.01  # degrees (~1 km head-sized tolerance)

    years_passed = 0
    step = 0

    print("Starting simulation...\n")

    while True:
        # Move entities yearly
        turtle.move()
        yoke.move(years_passed)

        years_passed += 1

        # Turtle surfaces every 100 years
        if years_passed % YEARS_PER_BREATH == 0:
            step += 1

            dist = distance_deg(
                turtle.lat, turtle.lon,
                yoke.lat, yoke.lon
            )

            print(
                f"Breath #{step} | "
                f"Years: {format_years(years_passed)} | "
                f"Turtle(lat={turtle.lat:.4f}, lon={turtle.lon:.4f}) | "
                f"Yoke(lat={yoke.lat:.4f}, lon={yoke.lon:.4f})"
            )

            if dist <= SUCCESS_RADIUS:
                print("\nSUCCESS!")
                print(f"Total years passed: {format_years(years_passed)}")
                break

        # Optional slowdown for readability (comment out if unwanted)
        # time.sleep(0.01)


if __name__ == "__main__":
    simulate()
