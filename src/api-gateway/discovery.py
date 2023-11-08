import time
import grpc
from concurrent import futures

from proto import discovery_pb2
from proto import discovery_pb2_grpc
from proto import login_pb2
from proto import login_pb2_grpc
from proto import searchnow_pb2
from proto import searchnow_pb2_grpc
from proto import searchpast_pb2
from proto import searchpast_pb2_grpc
from proto import searchforecast_pb2
from proto import searchforecast_pb2_grpc


class Microservice:
    def __init__(self, serviceName, port):
        self.serviceName = serviceName
        self.port = port

# who am I?
# Port:
PORT = '50050'
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

            channel = grpc.insecure_channel('login:'+port)
            stub = login_pb2_grpc.LoginnerStub(channel)
            login_reply = stub.Login(login_pb2.LoginRequest(username=request.username, password=request.password))


            if(login_reply.correct):
                return discovery_pb2.DiscoveryLoginReply(correct=True)

            return discovery_pb2.DiscoveryLoginReply(correct=False)
                              
        except:
            return discovery_pb2.DiscoveryLoginReply(correct=False)
    
    def discoverySearchPast(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            port = microservices['search_past']
            channel = grpc.insecure_channel('search-past:'+port)
            stub = searchpast_pb2_grpc.SearcherPastStub(channel)
            reply = stub.Search(searchpast_pb2.SearchPastRequest(city=request.city))
                    
            return discovery_pb2.DiscoverySearchPastReply(correct=True, city=reply.city, max_temperature=reply.max_temperature, min_temperature=reply.min_temperature, avg_temperature=reply.avg_temperature, max_humidity=reply.max_humidity, min_humidity=reply.min_humidity, avg_humidity=reply.avg_humidity, avg_cloudcover=reply.avg_cloudcover)
                              
        except Exception as e:
            fp = open("errori.txt", "a")
            fp.write("discovery search past: risposta errata"+str(e)+"\n")
            fp.close()
            return discovery_pb2.DiscoverySearchPastReply(correct=False)
    
    def discoverySearchNow(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            port = microservices['search_now']
            channel = grpc.insecure_channel('search-now:'+port)
            stub = searchnow_pb2_grpc.SearcherNowStub(channel)
            search_reply = stub.Search(searchnow_pb2.SearchNowRequest(city=request.city))
   
            return discovery_pb2.DiscoverySearchNowReply(correct=True, city=search_reply.city, temperature=search_reply.temperature, humidity=search_reply.humidity, cloudiness=search_reply.cloudiness)
                              
        except Exception as e:
            fp = open("errori.txt", "a")
            fp.write("discoverySearchNow: risposta errata"+str(e)+"\n")
            fp.close()
            return discovery_pb2.DiscoverySearchNowReply(correct=False)
        
    def discoverySearchForecast(self, request, context):
        try:
            # Verifico se è presente l'informazione richiesta.
            port = microservices['search_forecast']
            channel = grpc.insecure_channel('search-forecast:'+port)
            stub = searchforecast_pb2_grpc.SearcherForecastStub(channel)
            reply = stub.Search(searchforecast_pb2.SearchForecastRequest(city=request.city))

            days = [reply.day1, reply.day2, reply.day3, reply.day4, reply.day5]
            forecasts = []
            
            for i in range(0,5):
                
                daily_forecast = {
                    'date': "",
                    'max_temperature': -float('inf'),
                    'min_temperature': float('inf'),
                    'humidity': 0,
                    'weather': [],
                    'wind_speed': []
                }
                daily_forecast['date'] = days[i].date
                daily_forecast['max_temperature'] = days[i].max_temperature
                daily_forecast['min_temperature'] = days[i].min_temperature
                daily_forecast['humidity'] = days[i].humidity
                daily_forecast['weather'] = days[i].weather
                daily_forecast['wind_speed'] = days[i].wind_speed
                forecasts.append(daily_forecast)
        

            return discovery_pb2.DiscoverySearchForecastReply(correct=True, city=reply.city, day1=forecasts[0], day2=forecasts[1], day3=forecasts[2], day4=forecasts[3], day5=forecasts[4])
                              
        except Exception as e:
            fp = open("errori.txt", "a")
            fp.write("discovery forecast exception : "+str(e)+"\n")
            fp.close()
            return discovery_pb2.DiscoverySearchForecastReply(correct=False)


    """
    Register a microservice and the port where it's listening.
    """
    def put(self, request, context):

        try:
            # Registrazione nella cache della nuova istanza di microservizio
            microservices[request.serviceName] = request.port
            fp = open("discovery.txt", "a")
            fp.write("\n registrato sservizio: " + request.serviceName)
            fp.close()
        except ValueError:
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