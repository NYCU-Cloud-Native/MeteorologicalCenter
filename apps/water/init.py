# -*- coding: utf-8 -*-
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

name_table = {"10201": "石門水庫", "10203": "西勢水庫", "10204":"新山水庫", "10205":"翡翠水庫","10206":"榮華壩", "10207" :"鳶山堰", "10209" :"桂山壩", "10210" :"三峽攔河堰", "10211" :"青潭堰", "10212" :"直潭壩", "10213" :"羅好壩", "10214" :"阿玉壩", "10401" :"寶山水庫", "10404" :"隆恩堰", "10405" :"寶山第二水庫", "10501" :"永和山水庫", "10503" :"大埔水庫", "10601" :"明德水庫", "10802" :"羅東攔河堰", "20101" :"鯉魚潭水庫", "20201" :"德基水庫", "20202" :"石岡壩", "20405" :"士林攔河堰", "20501" :"霧社水庫", "20502" :"日月潭水庫", "20503" :"集集攔河堰", "20508" :"明湖下池水庫", "20509" :"湖山水庫", "30301" :"仁義潭水庫", "30302" :"蘭潭水庫", "30306" :"內埔子水庫", "30401" :"白河水庫", "30403" :"德元埤水庫", "30501" :"烏山頭水庫", "30502" :"曾文水庫", "30503" :"南化水庫", "30504" :"鏡面水庫", "30601" :"虎頭埤水庫", "30602" :"鹽水埤水庫", "30802" :"阿公店水庫", "30803" :"鳳山水庫", "30901" :"高屏溪攔河堰", "31002" :"甲仙攔河堰", "31201" :"牡丹水庫", "31301" :"成功水庫", "50102" :"興仁水庫", "50103" :"東衛水庫", "50104" :"赤崁地下水庫", "50105" :"西安水庫", "50106" :"七美水庫", "50108" :"小池水庫", "50109" :"烏溝蓄水塘", "50201" :"太湖水庫", "50202" :"田埔水庫", "50203" :"陽明湖水庫", "50204" :"山西水庫", "50205" :"榮湖水庫", "50206" :"擎天水庫", "50207" :"金沙水庫", "50208" :"蓮湖水庫", "50209" :"菱湖水庫", "50210" :"西湖水庫", "50212" :"金湖水庫", "50213" :"瓊林水庫", "50214" :"蘭湖", "50301" :"勝利水庫", "50302" :"秋桂山水庫", "50303" :"珠螺水壩", "50304" :"儲水沃上壩", "50305" :"儲水沃水庫", "50306" :"津沙水庫", "50307" :"津沙一號水庫", "50308" :"坂里水庫", "50309" :"東湧水庫", "50310" :"后沃水庫"}

if response.status_code == 200:
    f_reader = response.text.split('\r\n')[1:-1]
    reader = csv.reader(f_reader)

    for row in reader:
        try:
            next_row = next(reader)

            if row[10] != next_row[10]:
                print(row)
                # Create a data point
                data_point = Point("reservoir-4") \
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
                    .field("ReservoirName", name_table[row[10]]) \
                    .field("SpillwayOutflow", row[11]) \
                    .field("StatusType", row[12]) \
                    .field("TotalOutflow", row[13]) \
                    .field("WaterDraw", row[14]) \
                    .field("WaterLevel", row[15]) 

                write_api.write(bucket=bucket, org=org, record=[data_point])
        except StopIteration:
            print(row)
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
            break

# Close the InfluxDB client
client.close()
