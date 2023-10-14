import grpc
import sys
import logging
import time

from proto import Registration_pb2
from proto import Registration_pb2_grpc
from proto import Discovery_pb2
from proto import Discovery_pb2_grpc


ADDR_PORT = ''
DISCOVERY_SERVER = 'code_discovery_2:50060'


class Output:
    def __init__(self, storedType, isCorrect):
        self.isCorrect = isCorrect
        self.storedType = storedType




"""
Ha il compito di recuperare la porta su cui
il microservizio registration è in ascolto.
"""
def discovery_registration():
    global ADDR_PORT
    """
    Si tenta di contattare il discovery server registrato
    per ottenere la porta su cui il servizio di registration è in
    ascolto. Se la chiamata dovesse fallire, si attendono 5
    secondi per poi eseguire nuovamente il tentativo di connessione.
    """
    while(True):
        try:
            # Provo a connettermi al server.
            channel = grpc.insecure_channel(DISCOVERY_SERVER)
            stub = Discovery_pb2_grpc.DiscoveryServiceStub(channel)
            # Ottengo la porta su cui il microservizio di Registration è in ascolto.
            res = stub.get(Discovery_pb2.GetRequest(serviceName="frontend" , serviceNameTarget="registration"))
            if (res.port == -1):
                # Il discovery server ancora non è a conoscenza della porta richiesta.
                time.sleep(5)
                continue            
            ADDR_PORT = res.serviceName + ':' + res.port
            break
        except:
            # Problema nella connessione con il server.
            time.sleep(5)
            continue