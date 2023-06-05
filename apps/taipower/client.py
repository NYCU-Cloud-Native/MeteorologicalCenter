import grpc
import power_data_pb2
import power_data_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = power_data_pb2_grpc.PowerDataServiceStub(channel)
    response = stub.GetPowerDataInfo(power_data_pb2.PowerDataRequest())
    print("CSV URL:", response.csvUrl)

if __name__ == '__main__':
    run()
