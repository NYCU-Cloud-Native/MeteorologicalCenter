import grpc
from concurrent import futures
import crawler_pb2
import crawler_pb2_grpc
import requests
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

class CrawlerServicer(crawler_pb2_grpc.CrawlerServicer):
    def Run(self, request, context):
        load_dotenv()

        url = os.getenv('DB_URL')
        token = os.getenv('DB_TOKEN')
        org = os.getenv('DB_ORG')
        bucket = os.getenv('DB_BUCKET')
        data_url = os.getenv('DATA_URL')
        # Create InfluxDB client
        client = InfluxDBClient(url=url, token=token, org=org)

        # Create the write API
        write_api = client.write_api(write_options=SYNCHRONOUS)

        data_points = []
        # Fetch data from URL
        response = requests.get(data_url)

        if response.status_code == 200:    
            reader = response.text.split('\r\n')[1:-1]
            
            for row in reader:
                x = row.replace('"', '').split(',')
                print(x)
                # Create a data point
                data_point = Point("reservoir") \
                    .field("CatchmentAreaRainfall", x[0]) \
                    .field("DesiltingTunnelOutflow", x[1]) \
                    .field("DrainageTunnelOutflow", x[2]) \
                    .field("EffectiveWaterStorageCapacity", x[3]) \
                    .field("InflowDischarge", x[4]) \
                    .field("ObservationTime", x[5]) \
                    .field("OthersOutflow", x[6]) \
                    .field("PowerOutletOutflow", x[7]) \
                    .field("PredeterminedCrossFlow", x[8]) \
                    .field("PredeterminedOutflowTime", x[9]) \
                    .tag("ReservoirIdentifier", x[10])\
                    .field("SpillwayOutflow", x[11]) \
                    .field("StatusType", x[12]) \
                    .field("TotalOutflow", x[13]) \
                    .field("WaterDraw", x[14]) \
                    .field("WaterLevel", x[15]) 

                write_api.write(bucket=bucket, org=org, record=[data_point])

                # Close the InfluxDB client
                client.close()
                print("Data successfully written to InfluxDB")
                print(crawler_pb2.Response())
                return crawler_pb2.Response()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crawler_pb2_grpc.add_CrawlerServicer_to_server(CrawlerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
