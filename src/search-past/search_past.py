import time
import grpc
from concurrent import futures

from proto import searchpast_pb2
from proto import searchpast_pb2_grpc
import searchPastDiscovery

import requests
from circuitbreaker import circuit
from calculator import *
from cache import *
import datetime
import ast

#from redis import Redis

# who am I?
# Port:
PORT = '50052'
NAME = 'search_past'



class SearcherPast(searchpast_pb2_grpc.SearcherPastServicer):
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

        city = request.city

        # get cached data based on city name
        res = getCachedCity(city)
        fp = open("cache.txt", "a")
        fp.write("ecco cosa c'era su redis rispetto alla city: "+str(res))
        fp.close()

        if(res == None):
            # Calcola la data attuale e la data di una settimana fa
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=7)

            # Configura l'URL per la richiesta a Visual Crossing
            api_key = 'N92B2LKMTPMGZWLS7MVMWWETY'
            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&key={api_key}'
            
            # Effettua una richiesta GET ai dati meteorologici storici
            response = requests.get(url)
            # eventually throws exception to close the circuit
            response.raise_for_status()
            
            data = response.json()
            # Estrarre i dati di interesse dalla risposta
            historical_data = data['days']

            # Calcolare le statistiche dal DataFrame
            max_temperature = []
            min_temperature = []
            avg_temperature = []
            max_humidity = []
            min_humidity = []
            avg_humidity = []
            avg_cloudcover = []

            for i in range(0,5):
                max_temperature.append(historical_data[i]['tempmax'])
                min_temperature.append(historical_data[i]['tempmin'])
                avg_temperature.append(historical_data[i]['feelslike'])
                max_humidity.append(historical_data[i]['humidity'])
                min_humidity.append(historical_data[i]['humidity'])
                avg_humidity.append(historical_data[i]['humidity'])
                avg_cloudcover.append(historical_data[i]['cloudcover'])

            max_temp = maximum(max_temperature)
            min_temp = minimum(min_temperature)
            avg_temp = avg(avg_temperature)
            max_hum = maximum(max_humidity)
            min_hum = minimum(min_humidity)
            avg_hum = avg(avg_humidity)
            avg_clo = avg(avg_cloudcover)

            cityData = {
                'max_temp': max_temp,
                'min_temp': min_temp,
                'avg_temp': avg_temp,
                'max_hum': max_hum,
                'min_hum': min_hum,
                'avg_hum': avg_hum,
                'avg_clo': avg_clo
            }
            # Salva in cache
            res = cacheCity(city, cityData)

            return searchpast_pb2.SearchPastReply(city=city, max_temperature=float(max_temp), min_temperature=float(min_temp), avg_temperature=float(avg_temp), max_humidity=float(max_hum), min_humidity=float(min_hum), avg_humidity=float(avg_hum), avg_cloudcover=float(avg_clo))

        else:
            fp = open("errorichache.txt", "a")
            fp.write("ecco res: "+res)
            fp.close()
            # no need to cache, we already got the data
            # just convert the string to dict
            # and slicing off the first char because it's bytes
            cityData = ast.literal_eval(ast.literal_eval(str(res)[1:]))
            return searchpast_pb2.SearchPastReply(city=city, max_temperature=float(cityData['max_temp']), min_temperature=float(cityData['min_temp']), avg_temperature=float(cityData['avg_temp']), max_humidity=float(cityData['max_hum']), min_humidity=float(cityData['min_hum']), avg_humidity=float(cityData['avg_hum']), avg_cloudcover=float(cityData['avg_clo']))

            

    

# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
searchpast_pb2_grpc.add_SearcherPastServicer_to_server(SearcherPast(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    searchPastDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)
