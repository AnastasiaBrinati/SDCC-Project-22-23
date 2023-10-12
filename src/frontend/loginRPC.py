import grpc
import sys
import logging
import time

from proto import login_pb2
from proto import login_pb2_grpc


"""
Instanzia un canale di comunicazione con il
microservizio che gestisce le iscrizioni per
l'applicazione. Viene passato in input un
messaggio contenente tutte le informazioni
necessarie per l'iscrizione.
"""
def sendLoginInfo(username):
    """
    Verifico se il frontend già è a conoscenza della porta
    su cui contattare il micorservizio di registration.
    """
    
    #if (ADDR_PORT == ''):
    #    discovery_registration()

    ADDR_PORT = "localhost:50051"

    channel = grpc.insecure_channel(ADDR_PORT)
    stub = login_pb2_grpc.LoginnerStub(channel)

    """
    Invio della richiesta di iscrizione dell'utente.
    Il valore di output sarà TRUE se è andata a buon
    fine; altrimenti, sarà FALSE.(?)
    """

    output = stub.SayHello(login_pb2.HelloRequest(name=username))
    print(output)

    return output