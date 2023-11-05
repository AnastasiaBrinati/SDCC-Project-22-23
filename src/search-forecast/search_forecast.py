import time
import grpc
from concurrent import futures

from proto import searchforecast_pb2
from proto import searchforecast_pb2_grpc
import searchForecastDiscovery

import requests
from circuitbreaker import circuit

# who am I?
# Port:
PORT = '50054'
NAME = 'search_forecast'

class SearcherForecast(searchforecast_pb2_grpc.SearcherForecastServicer):
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
        # Imposta la chiave API di OpenWeatherMap
        api_key = "b8b7a2ac64b15fd3fd5f87d885b16e5b"
        # Esegui una richiesta per ottenere i dati meteo della prossima settimana
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Unità di misura metrica (Celsius, km/h)
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        # se request non va a buon fine, dovrebbe aprirsi il circuit
        data = response.json()
   
        # Estrai la lista delle previsioni giornaliere
        daily_forecasts = []
        current_date = None
   
        for forecast in data['list']:
            forecast_date = forecast['dt_txt'].split()[0]
   
            # Se la data è cambiata, crea un nuovo dizionario per il giorno corrente
            if forecast_date != current_date:
                current_date = forecast_date
                daily_forecast = {
                    'date': forecast_date,
                    'max_temperature': -float('inf'),
                    'min_temperature': float('inf'),
                    'humidity': 0,
                    'weather': [],
                    'wind_speed': []
                }
                daily_forecasts.append(daily_forecast)
   
            # Aggiorna i dati del giorno corrente
            daily_forecast['max_temperature'] = max(daily_forecast['max_temperature'], forecast['main']['temp_max'])
            daily_forecast['min_temperature'] = min(daily_forecast['min_temperature'], forecast['main']['temp_min'])
            daily_forecast['humidity'] += forecast['main']['humidity']
            daily_forecast['weather'].append(forecast['weather'][0]['description'])
            daily_forecast['wind_speed'].append(forecast['wind']['speed'])
   
        # Calcola le medie e le mode
        for daily_forecast in daily_forecasts:
            daily_forecast['humidity'] /= len(daily_forecast['weather'])
            daily_forecast['weather'] = max(set(daily_forecast['weather']), key=daily_forecast['weather'].count)
            daily_forecast['wind_speed'] = sum(daily_forecast['wind_speed']) / len(daily_forecast['wind_speed'])


        return searchforecast_pb2.SearchForecastReply(city=city, day1=daily_forecasts[0], day2=daily_forecasts[1], day3=daily_forecasts[2], day4=daily_forecasts[3], day5=daily_forecasts[4])

# To monitor your circuits: 
# CircuitBreakerMonitor.get_circuits()
# because they auto-report infos 
# CircuitBreakerMonitor.all_closed()
# CircuitBreakerMonitor.get_open()
# CircuitBreakerMonitor.get_closed()

# Creazione del server RPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
searchforecast_pb2_grpc.add_SearcherForecastServicer_to_server(SearcherForecast(), server)

# Avvio del server RPC.
server.add_insecure_port('[::]:' + PORT)
server.start()

try:
    searchForecastDiscovery.serve(PORT, NAME)
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
        server.stop(0)