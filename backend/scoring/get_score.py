import os
from dotenv import load_dotenv
from services.snowflake import SnowflakeService
import math
load_dotenv()



EARTH_RADIUS_KM = 6371


def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def score_guess(
    guess_lat: float,
    guess_lon: float,
    sightings: list[tuple[float, float]],
) -> dict:
    """
    sightings: [(lat, lon), ...]
    """

    # 1️⃣ Compute centroid
    lat_c = sum(lat for lat, _ in sightings) / len(sightings)
    lon_c = sum(lon for _, lon in sightings) / len(sightings)

    # 2️⃣ Compute max_radius_km (species spread)
    max_radius_km = 0.0
    min_distance_km = float("inf")

    for lat, lon in sightings:
        # distance to centroid → for max radius
        d_centroid = haversine(lat_c, lon_c, lat, lon)
        if d_centroid > max_radius_km:
            max_radius_km = d_centroid

        # distance to guess → for score
        d_guess = haversine(guess_lat, guess_lon, lat, lon)
        if d_guess < min_distance_km:
            min_distance_km = d_guess

    # 3️⃣ Safety clamp (important)
    max_radius_km = max(max_radius_km, 50.0)

    # 4️⃣ Normalize & score
    d_norm = min(min_distance_km / max_radius_km, 1.0)
    score = round(1000 * math.exp(-3 * d_norm))
    
    # helper: find the lat/lon of the closest point for UI
    closest_sighting = None
    min_dist_check = float("inf")
    
    for lat, lon in sightings:
        d = haversine(guess_lat, guess_lon, lat, lon)
        if d < min_dist_check:
            min_dist_check = d
            closest_sighting = {"lat": lat, "lng": lon}

    return {
        "score": score,
        "distance_km": round(min_distance_km, 2),
        "max_radius_km": round(max_radius_km, 2),
        "closest_sighting": closest_sighting
    }

    
