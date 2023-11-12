import time
import sys
import grpc
from concurrent import futures

from proto import user_pb2
from proto import user_pb2_grpc
import userDiscovery
import userDB

# who am I?
# Port:
PORT = '50051'
NAME = 'user'

class Userer(user_pb2_grpc.UsererServicer):
    def Login(self, request, context):
        res,cities = userDB.checkCredentials(request.username, request.password)
        if(not res):
            return user_pb2.LoginReply(correct=False)
        if len(cities) < 3:
            cities.append("")
            cities.append("")
            cities.append("")
        
        fp = open("citta.txt", "a")
        fp.write("citta1: " + cities[0])
        fp.write("\ncitta2: " + cities[1])
        fp.write("\ncitta3: " + cities[2])
        fp.close()
        return user_pb2.LoginReply(correct=True, city1=cities[0], city2=cities[1], city3=cities[3])
    
    def AddToFav(self, request, context):
        res = userDB.checkCredentials(request.username, request.city)
        if(not res):
            return user_pb2.AddToFavReply(correct=False)
        return user_pb2.AddToFavReply(correct=True)



# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
user_pb2_grpc.add_UsererServicer_to_server(Userer(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    userDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)