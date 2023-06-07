# -*- coding: utf-8 -*-
import unittest
from unittest import mock
import requests
import csv, os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class ReservoirDataTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        # Set up the connection parameters
        self.url = os.getenv('TEST_DB_URL')
        self.token = os.getenv('TEST_DB_TOKEN')
        self.org = os.getenv('TEST_DB_ORG')
        self.bucket = os.getenv('TEST_DB_BUCKET')
        self.data_url = os.getenv('TEST_DATA_URL')

        # Mock the InfluxDBClient
        self.client = mock.Mock(spec=InfluxDBClient)

    def test_data_retrieval(self):
        # Fetch the reservoir data
        reservoir_url = "https://data.wra.gov.tw/Service/OpenData.aspx?format=csv&id=1602CA19-B224-4CC3-AA31-11B1B124530F"
        response = requests.get(reservoir_url)
        
        # Ensure data retrieval is successful
        self.assertEqual(response.status_code, 200)

        if response.status_code == 200:
            f_reader = response.text.split('\r\n')[1:-1]
            csv_reader = csv.reader(f_reader)
            reader = list(csv_reader)

            # Assert that the retrieved data has the expected format or values
            self.assertGreater(len(reader), 0)

    def test_data_insertion(self):
        # Create the write API
        write_api = self.client.write_api.return_value
        
        # Define the measurement and tags
        reservoir_measurement = "reservoir_measurement"
        
        # Prepare the data points
        data_points = [
            Point(reservoir_measurement).tag("ReservoirIdentifier", "10203").field("TotalOutflow", 10).field("WaterDraw", 20),
            Point(reservoir_measurement).tag("ReservoirIdentifier", "2").field("TotalOutflow", 30).field("WaterDraw", 40)
        ]

        # Write the data points to InfluxDB
        write_api.write.return_value = None
        write_api.write.assert_not_called()  # Ensure the write method is not called directly
        write_api.write(bucket="mock_bucket", record=data_points)

    def test_close_influxdb_client(self):
        # Create a mock instance of InfluxDBClient
        self.client.close()
        
    def tearDown(self):
        # Clean up resources after the tests
        pass

if __name__ == '__main__':
    unittest.main()
