import time
import grpc
from proto import discovery_pb2
from proto import discovery_pb2_grpc

DISCOVERY_SERVER = 'api-gateway:50050'

"""
Expose microservice and it's port.
"""

# scrivi meglio e leva le cose di fanfa

# ---------------------------------------- DISCOVERY ---------------------------------------------
def serve(MY_PORT, MY_SERVER_NAME):
    """
    Si tenta di contattare il discovery server registrato
    per memorizzare la porta su cui il servizio di Registration è in
    ascolto. Se le chiamate dovessero fallire, si attendono 5
    secondi per poi eseguire nuovamente il tentativo di connessione.
    """
    ok = False
    while(True):
        # Itero sui discovery servers noti        
            try:
                # Provo a connettermi al server
                channel = grpc.insecure_channel(DISCOVERY_SERVER)
                stub = discovery_pb2_grpc.DiscoveryServiceStub(channel)
                put_reply = stub.put(discovery_pb2.PutRequest(serviceName=MY_SERVER_NAME , port=MY_PORT))
                ok = True
            except:
                # Si è verificato un problema nella connessione con il discovery server
                time.sleep(2)
                continue
            if(not put_reply.result):
                # Si è verificato un problema con DynamoDB
                time.sleep(2)
                continue
            if(ok):
                break
    return

# ---------------------------------------- DISCOVERY ---------------------------------------------