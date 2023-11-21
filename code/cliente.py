from locust import HttpUser, task, between
import time, random
lambd=1000
class HelloWorldUser(HttpUser):
    a=random.expovariate(lambd)
    wait_time = time.sleep(a)

    @task
    def hello_world(self):
        self.client.get("")