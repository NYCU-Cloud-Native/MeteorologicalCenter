from concurrent import futures
import logging

import grpc
from crawler import TaipowerCrawler


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    rpc_method_handlers = {
        'get_data': grpc.unary_unary_rpc_method_handler(
            TaipowerCrawler.get_data
        )
    }
    handler = grpc.method_handlers_generic_hand
    ler('crawler.TaipowerCrawler', rpc_method_handlers)

    server.add_generic_rpc_handlers((handler,))
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()