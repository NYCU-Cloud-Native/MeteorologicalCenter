# -*- coding: utf-8 -*-
import grpc
from concurrent import futures
import crawler_pb2
import crawler_pb2_grpc
import requests
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os, csv

class CrawlerServicer(crawler_pb2_grpc.CrawlerServicer):
    
    def insert_influxdb(reader):
        data_point = Point("reservoir-3") \
            .field("CatchmentAreaRainfall", reader[0]) \
            .field("DesiltingTunnelOutflow", reader[1]) \
            .field("DrainageTunnelOutflow", reader[2]) \
            .field("EffectiveWaterStorageCapacity", reader[3]) \
            .field("InflowDischarge", reader[4]) \
            .field("ObservationTime", reader[5]) \
            .field("OthersOutflow", reader[6]) \
            .field("PowerOutletOutflow", reader[7]) \
            .field("PredeterminedCrossFlow", reader[8]) \
            .field("PredeterminedOutflowTime", reader[9]) \
            .tag("ReservoirIdentifier", reader[10])\
            .field("SpillwayOutflow", reader[11]) \
            .field("StatusType", reader[12]) \
            .field("TotalOutflow", reader[13]) \
            .field("WaterDraw", reader[14]) \
            .field("WaterLevel", reader[15]) 
        return data_point

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

        # Fetch data from URL
        response = requests.get(data_url)

        # name table of reservoir
        name_table = {"10201": "石門水庫", "10203": "西勢水庫", "10204":"新山水庫", "10205":"翡翠水庫","10206":"榮華壩", "10207" :"鳶山堰", "10209" :"桂山壩", "10210" :"三峽攔河堰", "10211" :"青潭堰", "10212" :"直潭壩", "10213" :"羅好壩", "10214" :"阿玉壩", "10401" :"寶山水庫", "10404" :"隆恩堰", "10405" :"寶山第二水庫", "10501" :"永和山水庫", "10503" :"大埔水庫", "10601" :"明德水庫", "10802" :"羅東攔河堰", "20101" :"鯉魚潭水庫", "20201" :"德基水庫", "20202" :"石岡壩", "20405" :"士林攔河堰", "20501" :"霧社水庫", "20502" :"日月潭水庫", "20503" :"集集攔河堰", "20508" :"明湖下池水庫", "20509" :"湖山水庫", "30301" :"仁義潭水庫", "30302" :"蘭潭水庫", "30306" :"內埔子水庫", "30401" :"白河水庫", "30403" :"德元埤水庫", "30501" :"烏山頭水庫", "30502" :"曾文水庫", "30503" :"南化水庫", "30504" :"鏡面水庫", "30601" :"虎頭埤水庫", "30602" :"鹽水埤水庫", "30801": "澄清湖水庫", "30802" :"阿公店水庫", "30803" :"鳳山水庫", "30901" :"高屏溪攔河堰", "31002" :"甲仙攔河堰", "31201" :"牡丹水庫", "31301" :"成功水庫", "50102" :"興仁水庫", "50103" :"東衛水庫", "50104" :"赤崁地下水庫", "50105" :"西安水庫", "50106" :"七美水庫", "50108" :"小池水庫", "50109" :"烏溝蓄水塘", "50201" :"太湖水庫", "50202" :"田埔水庫", "50203" :"陽明湖水庫", "50204" :"山西水庫", "50205" :"榮湖水庫", "50206" :"擎天水庫", "50207" :"金沙水庫", "50208" :"蓮湖水庫", "50209" :"菱湖水庫", "50210" :"西湖水庫", "50212" :"金湖水庫", "50213" :"瓊林水庫", "50214" :"蘭湖", "50301" :"勝利水庫", "50302" :"秋桂山水庫", "50303" :"珠螺水壩", "50304" :"儲水沃上壩", "50305" :"儲水沃水庫", "50306" :"津沙水庫", "50307" :"津沙一號水庫", "50308" :"坂里水庫", "50309" :"東湧水庫", "50310" :"后沃水庫"}

        if response.status_code == 200:
            f_reader = response.text.split('\r\n')[1:-1]
            csv_reader = csv.reader(f_reader)
            reader = list(csv_reader)

            for i in range(len(reader)):
                try:
                    next_row = reader[i+1]
                    # if next data is not the same reservoir.
                    if reader[i][10] != next_row[10]:
                        # Create a data point
                        data_point = CrawlerServicer.insert_influxdb(reader[i])

                        write_api.write(bucket=bucket, org=org, record=[data_point])
                except :
                    # the last data of the reservoir
                    # Create a data point
                    data_point = CrawlerServicer.insert_influxdb(reader[i])

                    write_api.write(bucket=bucket, org=org, record=[data_point])
                    break

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
