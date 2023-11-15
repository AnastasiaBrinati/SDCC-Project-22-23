from locust import HttpUser, task,between, TaskSet
import json

class NowUser(HttpUser):
	wait_time = between(1,3)
	@task
	def search_now(self):
		headersFile = {'Content-Type':'application/json'}
		cookies = {'city':'Napoli'}
		response = None
		response = self.client.post("/search_now", data=json.dumps(cookies), headers=headersFile)
