import unittest
import pandas as pd
from loader import *


class TestLoader(unittest.TestCase):

    def test_valid_locations(self):

        geolocator = get_geolocator()

        locations = [
            "Museum of Modern Art",
            "USS Alabama Battleship Memorial Park"
        ]

        df = build_geo_dataframe(locations, geolocator)

        # Museum of Modern Art checks
        museum = df[df["location"] == "Museum of Modern Art"].iloc[0]

        self.assertAlmostEqual(museum["latitude"], 40.7618552, places=2)
        self.assertAlmostEqual(museum["longitude"], -73.9782438, places=2)
        self.assertEqual(museum["type"], "museum")

        # USS Alabama checks
        uss = df[df["location"] == "USS Alabama Battleship Memorial Park"].iloc[0]

        self.assertAlmostEqual(uss["latitude"], 30.684373, places=2)
        self.assertAlmostEqual(uss["longitude"], -88.015316, places=2)
        self.assertEqual(uss["type"], "park")

    def test_invalid_location(self):
        
        geolocator = get_geolocator()
        
        locations = ["asdfqwer1234"]

        df = build_geo_dataframe(locations, geolocator)

        row = df.iloc[0]

        self.assertEqual(row["location"], "asdfqwer1234")
        self.assertTrue(pd.isna(row["latitude"]))
        self.assertTrue(pd.isna(row["longitude"]))
        self.assertTrue(pd.isna(row["type"]))


if __name__ == "__main__":
    unittest.main()
