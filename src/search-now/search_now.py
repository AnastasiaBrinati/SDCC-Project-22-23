import time
import grpc
from concurrent import futures

from proto import searchnow_pb2
from proto import searchnow_pb2_grpc
import searchNowDiscovery

import requests
from circuitbreaker import circuit

# who am I?
# Port:
PORT = '50053'
NAME = 'search_now'

class SearcherNow(searchnow_pb2_grpc.SearcherNowServicer):
    # circuit is open:
    def negative_result(thrown_type, thrown_value):

        #429: too many requests
        #401: cliet error, unauthorized
        return issubclass(thrown_type, requests.HTTPError) and (thrown_value.status_code == 429 or thrown_value.status_code == 401)
    
    # MArtin Fowler implementation
    # recovery_timeout default : 30sec
    # name default: name of the function
    @circuit(failure_threshold=3, expected_exception=requests.RequestException, fallback_function=negative_result)
    def Search(self, request, context):
        api_key = "b8b7a2ac64b15fd3fd5f87d885b16e5b"  # Sostituisci con la tua chiave API di OpenWeatherMap
        url = f"https://api.openweathermap.org/data/2.5/weather"
        city = request.city

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Unità di misura metrica (Celsius, km/h)
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        temp = data.get("main", {}).get("temp")
        hum = data.get("main", {}).get("humidity")
        cloud = data.get("weather", [])[0].get("description")

        return searchnow_pb2.SearchNowReply(city=city, temperature=temp, humidity=hum, cloudiness=cloud)
    

# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
searchnow_pb2_grpc.add_SearcherNowServicer_to_server(SearcherNow(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    searchNowDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)