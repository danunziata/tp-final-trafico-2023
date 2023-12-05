from locust import HttpUser, task, between
import random, asyncio
#lambd=1000
class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        asyncio.sleep(0.01)
        self.client.get("/")