from fastapi import FastAPI
import random, asyncio
app = FastAPI()
mu = 100

@app.get("/")
async def root():
    a = random.expovariate(mu)
    asyncio.sleep(a)
    return {1}