from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os, csv, requests, pandas as pd
load_dotenv()

# Set up the connection parameters
url = os.getenv('DB_URL')
token = os.getenv('DB_TOKEN')
org = os.getenv('DB_ORG')
bucket = os.getenv('DB_BUCKET')
data_url = os.getenv('DATA_URL')

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

# Create the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Fetch data from URL
response = requests.get(data_url)

data_points = []
if response.status_code == 200:
    f_reader = response.text.split('\r\n')[1:-1]
    reader = csv.reader(f_reader)
    
    data_point = Point("reservoir-3") \
        .field("CatchmentAreaRainfall", reader[0][0]) \
        .field("DesiltingTunnelOutflow", reader[0][1]) \
        .field("DrainageTunnelOutflow", reader[0][2]) \
        .field("EffectiveWaterStorageCapacity", reader[0][3]) \
        .field("InflowDischarge", reader[0][4]) \
        .field("ObservationTime", reader[0][5]) \
        .field("OthersOutflow", reader[0][6]) \
        .field("PowerOutletOutflow", reader[0][7]) \
        .field("PredeterminedCrossFlow", reader[0][8]) \
        .field("PredeterminedOutflowTime", reader[0][9]) \
        .tag("ReservoirIdentifier", reader[0][10])\
        .field("SpillwayOutflow", reader[0][11]) \
        .field("StatusType", reader[0][12]) \
        .field("TotalOutflow", reader[0][13]) \
        .field("WaterDraw", reader[0][14]) \
        .field("WaterLevel", reader[0][15]) 
    write_api.write(bucket=bucket, org=org, record=[data_point])

    for row in len(reader):
        
        try:
            next_row = next(reader)
        
        # Create a data point
        data_point = Point("reservoir-3") \
            .field("CatchmentAreaRainfall", row[0]) \
            .field("DesiltingTunnelOutflow", row[1]) \
            .field("DrainageTunnelOutflow", row[2]) \
            .field("EffectiveWaterStorageCapacity", row[3]) \
            .field("InflowDischarge", row[4]) \
            .field("ObservationTime", row[5]) \
            .field("OthersOutflow", row[6]) \
            .field("PowerOutletOutflow", row[7]) \
            .field("PredeterminedCrossFlow", row[8]) \
            .field("PredeterminedOutflowTime", row[9]) \
            .tag("ReservoirIdentifier", row[10])\
            .field("SpillwayOutflow", row[11]) \
            .field("StatusType", row[12]) \
            .field("TotalOutflow", row[13]) \
            .field("WaterDraw", row[14]) \
            .field("WaterLevel", row[15]) 

        write_api.write(bucket=bucket, org=org, record=[data_point])

# Close the InfluxDB client
client.close()


