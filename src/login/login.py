import time
import grpc
from proto import login_pb2
from proto import login_pb2_grpc
from concurrent import futures


class Loginner(login_pb2_grpc.LoginnerServicer):
    def SayHello(self, request, context):
        return login_pb2.HelloReply(msg="Hello, %s!" % request.name)

def serve():
    port = "50051"
    #create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # server stub(?)
    login_pb2_grpc.add_LoginnerServicer_to_server(Loginner(), server)

    server.add_insecure_port("[::]:" + port)
    server.start()
    return server


try:
    server = serve()
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
    server.stop(0)