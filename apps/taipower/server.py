import grpc
from concurrent import futures
import power_data_pb2
import power_data_pb2_grpc
import pandas as pd
from influxdb import InfluxDBClient

class PowerDataServicer(power_data_pb2_grpc.PowerDataServiceServicer):
    def GetPowerDataInfo(self, request, context):
        csv_url = 'https://data.taipower.com.tw/opendata/apply/file/d006019/001.csv'

        # Read the CSV file
        df = pd.read_csv(csv_url)

        # Prepare the response
        response = power_data_pb2.PowerDataResponse()
        response.csvUrl = csv_url

        # Insert data to InfluxDB
        influx_host = 'localhost'  # Update with your InfluxDB host
        influx_port = 8086  # Update with your InfluxDB port
        influx_database = 'your_database'  # Update with your InfluxDB database name
        influx_measurement = 'power_data'  # Update with your desired measurement name

        client = InfluxDBClient(host=influx_host, port=influx_port)
        client.create_database(influx_database)
        client.switch_database(influx_database)

        lines = []
        for _, row in df.iterrows():
            for column in df.columns:
                lines.append(f'{column} value={row[column]}')

        influx_data = [{'measurement': influx_measurement, 'fields': {'value': line}} for line in lines]
        client.write_points(influx_data)

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
