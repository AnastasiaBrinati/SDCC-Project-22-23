import grpc
import time

from proto import discovery_pb2
from proto import discovery_pb2_grpc

"""
Known beforehand, you must have someplace to start the connection with the rest of the system
"""
DISCOVERY_SERVER = 'src-api-gateway-1:50060'

"""
Try to connect with the api-gateway to start the communication.
"""
def sendLoginInfo(username, password):
    """
    Attempting to connect to the api-gateway
    to communicate with the login service.
    In case of failure,
    another attempt will be made after 5s.
    """
    while(True):
        
        try:

            channel = grpc.insecure_channel(DISCOVERY_SERVER)
            stub = discovery_pb2_grpc.DiscoveryServiceStub(channel)
            # Connect with discovery server.
            res = stub.discoveryLogin(discovery_pb2.DiscoveryLoginRequest(serviceName="frontend", username=username))
            
            if (res == "-1"):
                # Discovery server not available.
                time.sleep(5)
                continue
            return res.validUsername
        
        except:
            # Problema nella connessione con il server.
            time.sleep(5)
            continue

