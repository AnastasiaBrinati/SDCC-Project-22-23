import time
import grpc
from concurrent import futures

from proto import search_pb2
from proto import search_pb2_grpc
import searchDiscovery

import requests
import json

# who am I?
# Port:
PORT = '50052'
NAME = 'search'

class Searcher(search_pb2_grpc.SearcherServicer):

    def Search(self, request, context):
        api_key = "b8b7a2ac64b15fd3fd5f87d885b16e5b"  # Sostituisci con la tua chiave API di OpenWeatherMap
        url = f"https://api.openweathermap.org/data/2.5/weather"
        cityName = request.city

        params = {
            "q": cityName,
            "appid": api_key,
            "units": "metric",  # Unità di misura metrica (Celsius, km/h)
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            temp = data.get("main", {}).get("temp")
            hum = data.get("main", {}).get("humidity")
            cloud = data.get("weather", [])[0].get("description")

            return search_pb2.SearchReply(correct=True, city=cityName, temperature=temp, humidity=hum, cloudiness=cloud)
        else:
            return search_pb2.SearchReply(correct=False, city=cityName)

    

# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
search_pb2_grpc.add_SearcherServicer_to_server(Searcher(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    searchDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)