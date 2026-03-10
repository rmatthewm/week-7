import unittest
import pandas as pd
from haversine import haversine, Unit
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        # Some known locations to test against
        known_loc1 = {"location": 'Museum of Modern Art', "latitude": 40.7618552, "longitude": -73.9782438, "type": 'museum'}
        known_loc2 = {"location": 'USS Alabama Battleship Memorial Park', "latitude": 30.684373, "longitude": -88.015316, "type": 'park'}

        # Get the geolocator
        geolocator = get_geolocator()

        # There is some slight difference between the coordinates returned by Nominatim
        # and those found using Google, so we will check that the coords are within a
        # certain distance.
        # The threshold of error in meters
        distance_threshold = 100

        # Test case 1
        result1 = fetch_location_data(geolocator, known_loc1['location'])
        # Use haversine to get the distance between the coords
        distance = haversine((result1['latitude'], result1['longitude']), 
                         (known_loc1['latitude'], known_loc1['longitude']), 
                         unit=Unit.METERS)
        self.assertLessEqual(distance, distance_threshold, 
                             f"Coords for test case 1 are more than {distance_threshold} meters away from the known location.")
        self.assertEqual(result1['type'], known_loc1['type'], 
                         "Type for test case 1 does not match.")

        # Test case 2
        result2 = fetch_location_data(geolocator, known_loc2['location'])
        # Use haversine to get the distance between the coords
        distance = haversine((result2['latitude'], result2['longitude']), 
                         (known_loc2['latitude'], known_loc2['longitude']), 
                         unit=Unit.METERS)
        self.assertLessEqual(distance, distance_threshold, 
                             f"Coords for test case 2 are more than {distance_threshold} meters away from the known location.")
        self.assertEqual(result2['type'], known_loc2['type'], 
                         "Type for test case 2 does not match.")

    def test_invalid_location(self):
        # Check that an invalid location has a row of NA values in the returned dataframe
        geolocator = get_geolocator()
        df = build_geo_dataframe(['asdfqwer1234'], geolocator)

        # Every value should be NA except for the location
        self.assertEqual(df['location'][0], 'asdfqwer1234')

        # We can check NAness using pandas and assert that is true
        self.assertTrue(df.isna()['latitude'][0], "Value should be NA.")
        self.assertTrue(df.isna()['longitude'][0], "Value should be NA.")
        self.assertTrue(df.isna()['type'][0], "Value should be NA.")

if __name__ == "__main__":
    unittest.main()
