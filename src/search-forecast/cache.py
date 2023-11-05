import redis
from datetime import datetime

def cacheCity(city, cityData):
  r = redis.Redis(host='cache', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')

  # imposta il timeout ai secondi che mancano fra ora e la fine della giornata
  now = datetime.now()
  end = datetime(now.year,now.month, now.day, 23,59,59)
  timeout =   (end-now).total_seconds()

  b = r.setex(city, int(timeout), str(cityData))

  r.close()
  # b: boolean
  return b

def getCachedCity(city):
  r = redis.Redis(host='cache', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
  res = r.get(city)
  r.close()
  return res
