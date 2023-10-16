import time
import sys
import grpc
from concurrent import futures

from proto import login_pb2
from proto import login_pb2_grpc
import loginDiscovery

# who am I?
# Port:
PORT = '50051'
# Name:
SERVER_1 = 'src-login-1'
# Me [in a list]: 
SERVERS = []

class Loginner(login_pb2_grpc.LoginnerServicer):
    def SayHello(self, request, context):
        return login_pb2.HelloReply(msg="Hello, %s!" % request.name)



# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
login_pb2_grpc.add_LoginnerServicer_to_server(Loginner(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    loginDiscovery.serve()
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)