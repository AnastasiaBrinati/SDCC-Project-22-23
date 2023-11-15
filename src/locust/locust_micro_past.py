from locust import HttpUser, task,between, TaskSet
import json

class PastUser(HttpUser):
	wait_time = between(1,3)	
	@task
	def search_past(self):
		headersFile = {'Content-Type':'application/json'}
		cookies = {'city':'Napoli'}
		response = None
		response = self.client.post("/search_past", data=json.dumps(cookies), headers=headersFile)