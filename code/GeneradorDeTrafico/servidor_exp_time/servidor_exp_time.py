from fastapi import FastAPI
import random, time
app = FastAPI()
mu = 100

@app.get("/")
async def root():
    a = random.expovariate(mu)
    time.sleep(a)
    return {1}