# created with from ChatGPT on 1/30/25
from assignment1 import *
import unittest
import pandas as pd
from io import StringIO
#import os
from unittest.mock import patch

class TestGeoFunctions(unittest.TestCase):
    # def test_user_input(self):
    #     user_input = os.getenv("TEST_USER_INPUT", "default_value")
    #     assert user_input == "default_value"

    def test_main_with_mocked_input(self):
        inputs = [
            "0",  # Choose manual input for first file
            "40.7128", "-74.0060", "n",  # One set of coordinates
            "0",  # Choose manual input for second file
            "34.0522", "-118.2437", "n",  # One set of coordinates
        ]
        with patch("builtins.input", side_effect=inputs):
            result = main()
        self.assertEqual(result, [[(40.7128, -74.006), (34.0522, -118.2437)]])

    def test_haversine(self):
        # Test known distance (New York City to Los Angeles)
        nyc = (40.7128, -74.0060)
        la = (34.0522, -118.2437)
        expected_distance = 3940  # Approximate distance in km
        result = haversine(nyc, la)
        self.assertAlmostEqual(result, expected_distance, delta=10)  # Allow small error margin

        # Same location should return zero
        self.assertEqual(haversine(nyc, nyc), 0)

    def test_match_closest(self):
        locations1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
        locations2 = [(41.8781, -87.6298), (29.7604, -95.3698)]  # Chicago, Houston

        # Expect NYC to be closest to Chicago, LA to Houston
        expected_output = [
            [(40.7128, -74.0060), (41.8781, -87.6298)],
            [(34.0522, -118.2437), (29.7604, -95.3698)]
        ]
        self.assertEqual(match_closest(locations1, locations2), expected_output)

    def test_clean_data(self):
        # Valid inputs
        self.assertEqual(clean_data(("40.7128N", "74.0060W")), (40.7128, -74.0060))
        self.assertEqual(clean_data(("34.0522S", "118.2437E")), (-34.0522, 118.2437))

        # Invalid latitude and longitude
        self.assertIsNone(clean_data(("100.1234N", "74.0060W")))  # Latitude out of bounds
        self.assertIsNone(clean_data(("40.7128N", "190.0000E")))  # Longitude out of bounds

        # Mixed input
        self.assertEqual(clean_data(("34.0522", "-118.2437")), (34.0522, -118.2437))

        # Invalid non-numeric input
        self.assertIsNone(clean_data(("invalid", "74.0060W")))
        self.assertIsNone(clean_data(("40.7128N", "invalid")))

    def test_clean_data_empty(self):
        # Empty input should return None
        self.assertIsNone(clean_data(("", "")))

    def test_clean_data_no_direction(self):
        # Already in correct format
        self.assertEqual(clean_data(("51.5074", "-0.1278")), (51.5074, -0.1278))  # London

    def test_clean_data_extra_spaces(self):
        # Should handle extra spaces
        self.assertEqual(clean_data((" 40.7128N ", " 74.0060W ")), (40.7128, -74.0060))

    def test_read_csv(self):
        # Simulate CSV input
        csv_data = """latitude,longitude
        40.7128,-74.0060
        34.0522,-118.2437
        """

        df = pd.read_csv(StringIO(csv_data))
        locations = list(zip(df["latitude"], df["longitude"]))
        expected_locations = [(40.7128, -74.0060), (34.0522, -118.2437)]
        self.assertEqual(locations, expected_locations)

if __name__ == '__main__':
    unittest.main()