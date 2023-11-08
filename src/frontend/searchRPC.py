import grpc

from proto import discovery_pb2
from proto import discovery_pb2_grpc

"""
Known beforehand, you must have someplace to start the connection with the rest of the system
"""
DISCOVERY_SERVER = 'api-gateway:50050'


def weatherNow(city):
    channel = grpc.insecure_channel(DISCOVERY_SERVER)
    stub = discovery_pb2_grpc.DiscoveryServiceStub(channel)
    reply = stub.discoverySearchNow(discovery_pb2.DiscoverySearchNowRequest(city=city))
    return [reply.temperature, reply.humidity, reply.cloudiness]



def weatherPast(city):
    channel = grpc.insecure_channel(DISCOVERY_SERVER)
    stub = discovery_pb2_grpc.DiscoveryServiceStub(channel)
    reply = stub.discoverySearchPast(discovery_pb2.DiscoverySearchPastRequest(city=city))
    return [reply.max_temperature, reply.min_temperature, reply.avg_temperature, reply.max_humidity, reply.min_humidity, reply.avg_humidity, reply.avg_cloudcover]



def weatherForecast(city):
    channel = grpc.insecure_channel(DISCOVERY_SERVER)
    stub = discovery_pb2_grpc.DiscoveryServiceStub(channel)
    # Connect with discovery server.
    reply = stub.discoverySearchForecast(discovery_pb2.DiscoverySearchForecastRequest(city=city))

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
            

    return forecasts
