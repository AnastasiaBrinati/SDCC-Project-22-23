from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 to 3 seconds between requests

    @task
    def forecast(self):

        # Define the payload for the login request
        payload = {
            "cityName": "Palermo"
        }

        # Define the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make a POST request to the login endpoint
        response = self.client.post("/forecast", json=payload, headers=headers)
