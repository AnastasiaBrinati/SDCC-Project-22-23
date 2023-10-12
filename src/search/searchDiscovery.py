from proto import Discovery_pb2
from proto import Discovery_pb2_grpc
import grpc
import time


# ---------------------------------------- DISCOVERY ---------------------------------------------
def put_discovery_server(discovery_servers, logger):
    new_discovery_servers = []
    """
    Si tenta di contattare il discovery server registrato
    per memorizzare la porta su cui il servizio di Registration è in
    ascolto. Se le chiamate dovessero fallire, si attendono 5
    secondi per poi eseguire nuovamente il tentativo di connessione.
    """
    ok = False
    while(True):
        # Itero sui discovery servers noti        
        for discovery_server in discovery_servers:
            try:
                # Provo a connettermi al server
                channel = grpc.insecure_channel(discovery_server)
                stub = Discovery_pb2_grpc.DiscoveryServiceStub(channel)
                # Memorizzo il servizio
                res = stub.put(Discovery_pb2.PutRequest(serviceName="registration" , port="50051"))
            except:
                # Si è verificato un problema nella connessione con il discovery server
                logger.info('[ PUT DISCOVERY REGISTRATION ] Problema connessione con il discovery server ' + discovery_server + '.')
                time.sleep(2)
                continue
            if(not res.result):
                # Si è verificato un problema con DynamoDB
                logger.info('[ PUT DISCOVERY REGISTRATION ] Problema DynamoDB con il discovery server ' + discovery_server + '.')
                time.sleep(2)
                continue
                
            for server in res.list_server.servers:
                new_discovery_servers.append(server)
            ok = True
            logger.info('[ PUT DISCOVERY REGISTRATION ] Registrazione avvenuta con successo presso il discovery server ' + discovery_server + '.')
            break
        if(ok):
            break
        logger.info('[ PUT DISCOVERY REGISTRATION ] Registrazione avvenuta con insuccesso presso tutti i discovery servers.')        
        time.sleep(5)       

    return new_discovery_servers

# ---------------------------------------- DISCOVERY ---------------------------------------------