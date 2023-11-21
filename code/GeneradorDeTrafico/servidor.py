from fastapi import FastAPI
import random
import time

app = FastAPI()
mu = 100    # 1 / media

@app.get("/")
async def root():
    b = time.time()
    a=random.expovariate(mu)
    time.sleep(a)
    return {time.time() - b}