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
NAME = 'login'

class Loginner(login_pb2_grpc.LoginnerServicer):
    def Login(self, request, context):
        return login_pb2.LoginReply(correct=True)



# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
login_pb2_grpc.add_LoginnerServicer_to_server(Loginner(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    loginDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)