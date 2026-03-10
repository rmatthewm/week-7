'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd


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
    """ Get the geographical data for a given location using the provided geolocator.

    Args:
        geolocator (Nominatim): a Nominatim instance 
        loc (str): a search string for the location

    Returns:
        dict or None: a dictionary with the location name, coords, and type;
        returns None if the location is not found
    """
    location = geolocator.geocode(loc)

    if location is None:
        return None
    
    return {"location": loc, "latitude": location.latitude, "longitude": location.longitude, "type": location.raw['type']}

def build_geo_dataframe(locations, geolocator):
    """ Build a pandas DataFrame with geographical data for the given locations.

    Args:
        locations (list): a list of location names
        geolocator (Nominatim): a Nominatim instance

    Returns:
        pandas.DataFrame: a DataFrame with the geographical data for the given locations
    """

    # We need to handle any missing data
    geo_data = []
    for loc in locations:
        loc_data = fetch_location_data(geolocator, loc)

        # If the data is not None, we can add it
        if loc_data is not None:
            geo_data.append(loc_data)

        # Otherwise, we can an empty entry 
        else:
            geo_data.append({"location": loc, "latitude": None, "longitude": None, "type": None})
        
    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]

    df = build_geo_dataframe(locations, geo)

    df.to_csv("./geo_data.csv")
