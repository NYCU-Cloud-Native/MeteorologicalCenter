import grpc
from concurrent import futures
import power_data_pb2
import power_data_pb2_grpc
import requests
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

class PowerDataServicer(power_data_pb2_grpc.PowerDataServiceServicer):
    def GetPowerDataInfo(self, request, context):
        load_dotenv()

        url = os.getenv('DB_URL')
        token = os.getenv('DB_TOKEN')
        org = os.getenv('DB_ORG')
        bucket = os.getenv('DB_BUCKET')

        # Create InfluxDB client
        client = InfluxDBClient(url=url, token=token, org=org)

        # Create the write API
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # Fetch data from URL
        response = requests.get(url)

        if response.status_code == 200:    
            reader = response.text.split('\n')[1:-1]

            for row in reader:
                row = row.split(',')
                timestamp = row[0]
                locations = ['North Generate', 'North Consumption', 'Central Generate', 'Central Consumption', 'South Generate', 'South Consumption', 'East Generate', 'East Consumption']
                values = {}

                for i, loc in enumerate(locations):
                    values.update({
                        loc: row[i+1]
                    })

                # Create a data point        
                for value in values:
                    point = Point("power_measurement")
                    point.tag("location", value)
                    point.field("_value", float(values[value]))
                    point.time(datetime.strptime(timestamp, "%Y-%m-%d %H:%M").isoformat())
                    
                    write_api.write(bucket=bucket, org=org, record=[point])

                # Close the InfluxDB client
                client.close()

                return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    power_data_pb2_grpc.add_PowerDataServiceServicer_to_server(PowerDataServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
