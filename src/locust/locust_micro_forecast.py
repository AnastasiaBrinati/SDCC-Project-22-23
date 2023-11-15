from locust import HttpUser, task,between, TaskSet
import json

class ForecastUser(HttpUser):
	wait_time = between(1,3)
	@task
	def search_forecast(self):
		headersFile = {'Content-Type':'application/json'}
		cookies = {'city':'Napoli'}
		response = None
		response = self.client.post("/search_forecast", data=json.dumps(cookies), headers=headersFile)