import time
import grpc
from concurrent import futures

from proto import discovery_pb2
from proto import discovery_pb2_grpc
from proto import login_pb2
from proto import login_pb2_grpc
from proto import search_pb2
from proto import search_pb2_grpc

# da sostituire con un db
microservices_db = []

class Microservice:
    def __init__(self, serviceName, port):
        self.serviceName = serviceName
        self.port = port

# who am I?
# Port:
PORT = '50050'
# Name:
SERVER_1 = 'src-api-gateway-1'
# [Me] in a list: 
SERVERS = []

# Cache contenente tutti gli oggetti Microservice che sono stati registrati.
microservices = {}


# Discovery Server
class DiscoveryServicer(discovery_pb2_grpc.DiscoveryServiceServicer):
    """
    Esposizione di un'api per i microservizi del sistema.
    """
    def discoveryLogin(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            port = microservices['login']

            fp = open("connection.txt", "a")
            fp.write("prima di chiamare\n")
            fp.close()
            
            channel = grpc.insecure_channel('src-login-1:'+port)
            stub = login_pb2_grpc.LoginnerStub(channel)
            login_reply = stub.Login(login_pb2.LoginRequest(username=request.username, password=request.password))

            fp = open("connection.txt", "a")
            fp.write("dopo la chiamata\n")
            fp.close()

            if(login_reply.correct):
                fp = open("connection.txt", "a")
                fp.write("risppsta corretta\n")
                fp.close()
                return discovery_pb2.DiscoveryLoginReply(correct=True)

            return discovery_pb2.DiscoveryLoginReply(correct=False)
                              
        except:
            return discovery_pb2.DiscoveryLoginReply(correct=False)
    
    def discoverySearch(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            port = microservices['search']

            channel = grpc.insecure_channel('src-search-1:'+port)
            stub = search_pb2_grpc.SearcherStub(channel)
            search_reply = stub.Search(search_pb2.SearchRequest(city=request.city))

            if(not search_reply.correct):
                return discovery_pb2.DiscoverySearchReply(correct=False)
                    
            return discovery_pb2.DiscoverySearchReply(correct=True, city=search_reply.city, temperature=search_reply.temperature, humidity=search_reply.humidity, cloudiness=search_reply.cloudiness)
                              
        except:
            return discovery_pb2.DiscoverySearchReply(correct=False)


    """
    Register a microservice and the port where it's listening.
    """
    def put(self, request, context):

        try:
            # Registrazione nella cache della nuova istanza di microservizio
            microservices[request.serviceName] = request.port
        except ValueError:
            file_log = open("put.txt", "a")
            file_log.write("\ndiscovery.py, put value error: "+ str(ValueError))
            file_log.close()
            return discovery_pb2.PutReply(result=False)
        
        # return Discovery_pb2.PutReply(result=True, list_server=discovery_servers)
        return discovery_pb2.PutReply(result=True)

# ---------------------------------------- STARTING SERVER DISCOVERY --------------------------------------------- #


# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
discovery_pb2_grpc.add_DiscoveryServiceServicer_to_server(DiscoveryServicer(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

# Main thread...
try:
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
    server.stop(0)