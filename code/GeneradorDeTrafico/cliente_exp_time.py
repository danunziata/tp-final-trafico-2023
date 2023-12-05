from locust import HttpUser, task, between
import time, random
lambd=1000
class HelloWorldUser(HttpUser):
   
	@task
	def hello_world(self):
		a=random.expovariate(lambd)
		time.sleep(a)
		self.client.get("/")
