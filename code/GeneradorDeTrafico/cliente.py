from locust import HttpUser, task, between
import random
lambd=1000
class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        self.client.get("")