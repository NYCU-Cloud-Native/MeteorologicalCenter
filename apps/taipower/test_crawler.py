import pytest
import grpc
import threading
import crawler_pb2
import crawler_pb2_grpc
import requests
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

from server import serve

# Define the test data for mocking the environment variables
mock_env_data = {
    'DB_URL': os.getenv('TEST_DB_URL'),
    'DB_TOKEN': os.getenv('TEST_DB_TOKEN'),
    'DB_ORG': os.getenv('TEST_DB_ORG'),
    'DB_BUCKET': os.getenv('TEST_DB_BUCKET'),
    'DATA_URL': os.getenv('TEST_DATA_URL')
}

class MockCrawlerServicer(crawler_pb2_grpc.CrawlerServicer):
    def Run(self, request, context):
        # Mock the environment variables
        os.getenv = lambda name: mock_env_data[name]

        # Mock the requests.get() method
        class MockResponse:
            def __init__(self, status_code, text):
                self.status_code = status_code
                self.text = text

        def mock_get(url):
            return MockResponse(200, '2023-06-06 12:00,1,2,3,4,5,6,7,8')

        requests.get = mock_get

        # Mock the InfluxDB client
        class MockInfluxDBClient:
            def __init__(self, url, token, org):
                pass

            def write_api(self, write_options):
                return MockWriteApi()

            def close(self):
                pass

        class MockWriteApi:
            def write(self, bucket, org, record):
                pass

        class MockPoint:
            def __init__(self, measurement):
                pass

            def tag(self, key, value):
                pass

            def field(self, key, value):
                pass

            def time(self, time):
                pass

        # Replace the original classes with the mock classes
        global InfluxDBClient, Point
        InfluxDBClient = MockInfluxDBClient
        Point = MockPoint

        # Run the gRPC method
        servicer = CrawlerServicer()
        response = servicer.Run(None, None)

        # Assert the response
        assert isinstance(response, crawler_pb2.Response)

# Pytest function to test the gRPC server
def test_grpc_server():
    # Start the gRPC server in a separate thread
    server_thread = threading.Thread(target=serve)
    server_thread.start()

    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = crawler_pb2_grpc.CrawlerStub(channel)

    # Call the gRPC method
    response = stub.Run(crawler_pb2.Request())

    # Assert the response
    assert isinstance(response, crawler_pb2.Response)

    # Stop the gRPC server
    channel.close()
    server_thread.join()

# Run the pytest
if __name__ == '__main__':
    pytest.main(['-v'])