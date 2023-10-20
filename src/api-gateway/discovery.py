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
all_microservices_cache = []

# Cache contenente tutti i nomi dei microservizi che sono stati registrati.
all_microservices_cache_names = []


# Discovery Server
class DiscoveryServicer(discovery_pb2_grpc.DiscoveryServiceServicer):
    """
    Esposizione di un'api per i microservizi del sistema.
    """
    def discoveryLogin(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            all_microservices_cache_names.index("login")
            
            # Cerco la porta relativa al microservizio richiesto.
            for m in all_microservices_cache:
                if m.serviceName == "login":

                    channel = grpc.insecure_channel('src-'+m.serviceName+'-1:'+m.port)
                    stub = login_pb2_grpc.LoginnerStub(channel)
                    login_reply = stub.Login(login_pb2.LoginRequest(username=request.username, password=request.password))

                    return discovery_pb2.DiscoveryLoginReply(correct=login_reply.correct)
                              
        except:
            """
            Il Discovery server ancora non è a conoscenza
            delle informazioni relative al microservizio richiesto.
            """
            return discovery_pb2.DiscoveryLoginReply(correct=False)
    
    def discoverySearch(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            all_microservices_cache_names.index("search")
            
            # Cerco la porta relativa al microservizio richiesto.
            for m in all_microservices_cache:
                if m.serviceName == "search":

                    channel = grpc.insecure_channel('src-'+m.serviceName+'-1:'+m.port)
                    stub = search_pb2_grpc.SearcherStub(channel)
                    search_reply = stub.Search(search_pb2.SearchRequest(city=request.city))

                    return discovery_pb2.DiscoverySearchReply(correct=search_reply.correct)
                              
        except:
            """
            Il Discovery server ancora non è a conoscenza
            delle informazioni relative al microservizio richiesto.
            """
            return discovery_pb2.DiscoverySearchReply(correct=False)


    """
    Register a microservice and the port where it's listening.
    """
    def put(self, request, context):

        try:
            """
            Check to see if the microservice is already registered.
            """
            all_microservices_cache_names.index(request.serviceName)
        except ValueError:

            """
            Microservice not registered.
            Save info about port and name of the microservice.
            """
            try:
                # da sostituire con il salvataggio su db
                microservice = Microservice(request.serviceName, request.port)
                microservices_db.append(microservice)
            except Exception:
                # Avviso il microservizio che si è verificato un errore nella PUT
                return discovery_pb2.PutReply(result=False)

            # in cache, locale per velocizzare
            # Creazione della nuova istanza di microservizio
            microservice = Microservice(request.serviceName, request.port)
            # Registrazione nella cache della nuova istanza di microservizio            
            all_microservices_cache.append(microservice)
            all_microservices_cache_names.append(microservice.serviceName)
            file_log = open("put.txt", "a")
            file_log.write("dentro discovery.py, put: "+request.serviceName)
        
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