import unittest
import requests
import csv
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()


class ReservoirDataTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the connection parameters
        self.url = os.getenv('DB_URL')
        self.token = os.getenv('DB_TOKEN')
        self.org = os.getenv('DB_ORG')
        self.bucket = os.getenv('DB_BUCKET')
        self.data_url = os.getenv('DATA_URL')

        # Connect to InfluxDB
        self.client = InfluxDBClient(url=self.url, token=self.token)

    def test_data_retrieval(self):
        # Fetch the reservoir data
        reservoir_url = "https://data.wra.gov.tw/Service/OpenData.aspx?format=csv&id=1602CA19-B224-4CC3-AA31-11B1B124530F"
        response = requests.get(reservoir_url)
        f_reader = response.text.split('\r\n')[1:-1]
        csv_reader = csv.reader(f_reader)
        reader = list(csv_reader)

        # Ensure data retrieval is successful
        self.assertEqual(response.status_code, 200)

    def test_data_insertion(self):
        # Fetch the reservoir data
        reservoir_url = "https://data.wra.gov.tw/Service/OpenData.aspx?format=csv&id=1602CA19-B224-4CC3-AA31-11B1B124530F"
        response = requests.get(reservoir_url)
        f_reader = response.text.split('\r\n')[1:-1]
        csv_reader = csv.reader(f_reader)
        data = list(csv_reader)

        # Additional assertions specific to data insertion

        # Create the write API
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        # Define the measurement and tags
        measurement = "reservoir-test"

        # Prepare the data points
        data_points = []
        for row in data:
            # Create a data point for each row
            data_point = Point(measurement).tag("tag1", "10201").field("field1", row[0]).field("field2", row[1])

            data_points.append(data_point)

        # Write the data points to InfluxDB
        write_api.write(bucket=self.bucket, org=self.org, record=data_points)

        # Query the data from InfluxDB
        query = f'from(bucket: "{self.bucket}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "{measurement}")'
        tables = self.client.query_api().query(query, self.org)
        
        pass


    def tearDown(self):
        # Clean up resources after the tests
        # For example, you can delete the test data from InfluxDB
        pass


if __name__ == '__main__':
    unittest.main()
