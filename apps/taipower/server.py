import grpc
from concurrent import futures
import crawler_pb2
import crawler_pb2_grpc
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

class CrawlerServicer(crawler_pb2_grpc.CrawlerServicer):

    def __init__(self):
        self.url = os.getenv('DB_URL')
        self.token = os.getenv('DB_TOKEN')
        self.bucket = os.getenv('DB_BUCKET')
        self.org = os.getenv('DB_ORG')
        self.data_url = os.getenv('DATA_URL')

    def Run(self, request, context):
        load_dotenv()

        self.url = os.getenv('DB_URL')
        self.token = os.getenv('DB_TOKEN')
        self.bucket = os.getenv('DB_BUCKET')
        self.org = os.getenv('DB_ORG')
        self.data_url = os.getenv('DATA_URL')

        # Create InfluxDB client
        client = InfluxDBClient(url=self.url, token=self.token, org=self.org)

        # Create the write API
        write_api = client.write_api(write_options=SYNCHRONOUS)

        values, timestamp = self._data_parser(self.data_url)

        for value in values:
            query = self._generate_query(value, values[value], timestamp)
            write_api.write(bucket=self.bucket, org=self.org, record=[query])

        # Close the InfluxDB client
        client.close()
        print("Data successfully written to InfluxDB")
        print(crawler_pb2.Response())
        return crawler_pb2.Response()

    def _generate_query(self, location, value, timestamp):
        point = Point(self.bucket)
        point.tag("location", location)
        
        try:
            point.field("value", float(value))
        except ValueError as e:
            print(f"ERROR: {e}")
            return None

        tp = pytz.timezone('Asia/Taipei')

        point.time(datetime.strptime(timestamp, "%Y-%m-%d %H:%M").replace(tzinfo=tp).isoformat())
        return point

    def _data_parser(self, url):

        # Fetch data from URL
        response = requests.get(url)
        values = {}
        timestamp = None

        if response.status_code == 200:    
            reader = response.text.split('\r\n')[1:-1]
            print(response.text.split('\r\n'))
            for row in reader:
                row = row.split(',')
                timestamp = row[0]
                locations = ['North Generate', 'North Consumption', 'Central Generate', 'Central Consumption', 'South Generate', 'South Consumption', 'East Generate', 'East Consumption']
                values = {}

                for i, loc in enumerate(locations):
                    values.update({
                        loc: row[i+1]
                    })

        return values, timestamp

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crawler_pb2_grpc.add_CrawlerServicer_to_server(CrawlerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
