from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

url = os.getenv('DB_URL')
token = os.getenv('DB_TOKEN')
org = os.getenv('DB_ORG')
bucket = os.getenv('DB_BUCKET')

# Create InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Create the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Open the CSV file
with open('001.csv', 'r') as f:
    reader = f.read().split('\n')[1:-1]

    for row in reader:
        row = row.split(',')
        timestamp = row[0]
        locations = ['North Generate', 'North Consumption', 'Central Generate', 'Central Consumption', 'South Generate', 'South Consumption', 'East Generate', 'East Consumption']
        values = {}

        for i, loc in enumerate(locations):
            values.update({
                loc: row[i+1]
            })

        print(values, timestamp)
        # Create a data point
        
        for value in values:
            point = Point("power_measurement")
            point.tag("location", value)
            point.field("_value", float(values[value]))
            point.time(datetime.strptime(timestamp, "%Y-%m-%d %H:%M").isoformat())
            
            write_api.write(bucket=bucket, org=org, record=[point])


# Close the InfluxDB client
client.close()
