import time
import grpc
from concurrent import futures

from proto import search_pb2
from proto import search_pb2_grpc
import searchDiscovery

# who am I?
# Port:
PORT = '50052'
NAME = 'search'

class Searcher(search_pb2_grpc.SearcherServicer):
    def Search(self, request, context):
        return search_pb2.SearchReply(correct=True)



# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
search_pb2_grpc.add_SearcherServicer_to_server(Searcher(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    searchDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)