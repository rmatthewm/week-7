'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd

"""
A note about refactoring to be a class. I don't think it makes sense to pass
in the geolocator into each method because I think the class should serve as
a wrapper for the Nominatim instance and so it should already have an instance.
But I don't know how much changing from the original assignment is acceptable
especially given the autograder. 
"""

class GeoLoader:
    """A wrapper for retrieving pandas.DataFrame-formatted data from Nominatim"""

    def __init__(self, agent='h501-student'):
        """ Initialize the class to have a Nominatim geocoder instance.

        Args:
            agent (str, optional): the agent to use for the geocoder. Defaults to 'h501-student'.
        """
        self.__agent = agent
        self.__geolocator = Nominatim(user_agent=self.__agent)

    def get_geolocator(self, agent='h501-student'):
        """
        Return the Nominatim instance or create a new one with a new agent name.

        Parameters
        ----------
        agent : str, optional
            Agent name for Nominatim, by default 'h501-student'
        """
        # If the agent name given matches what we already used, just return
        # the current instance 
        if agent == self.__agent:
            return self.__geolocator

        return Nominatim(user_agent=agent)

    def fetch_location_data(self, geolocator, loc):
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

    def build_geo_dataframe(self, locations, geolocator):
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
            loc_data = self.fetch_location_data(geolocator, loc)

            # If the data is not None, we can add it
            if loc_data is not None:
                geo_data.append(loc_data)

            # Otherwise, we can add an empty entry for this location
            else:
                geo_data.append({"location": loc, "latitude": pd.NA, "longitude": pd.NA, "type": pd.NA})
            
        return pd.DataFrame(geo_data)


if __name__ == "__main__":
    loader = GeoLoader()
    geo = loader.get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]

    df = loader.build_geo_dataframe(locations, geo)

    df.to_csv("./geo_data.csv")
