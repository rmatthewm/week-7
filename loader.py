'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)

def fetch_location_data(geolocator, loc):
    
    try:
        location = geolocator.geocode(loc)
    except Exception:
        location = None
    
    if location is None:
        return {
        "location": loc,
        "latitude": np.nan,
        "longitude": np.nan,
        "type": np.nan,
    }

    return {
        "location": loc,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "type": location.raw.get("type"),
    }

def build_geo_dataframe(locations, geolocator):
    
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]

            
    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    
    geo = get_geolocator()

    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa"
    ]
    
    df = build_geo_dataframe(locations, geo)

    df.to_csv("./geo_data.csv", index=False)