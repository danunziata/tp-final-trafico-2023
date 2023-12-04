from fastapi import FastAPI
import random
import asyncio

app = FastAPI()
mu = 100    # 1 / media

@app.get("/")
async def root():
    a=random.expovariate(mu)
    asyncio.sleep(a)
    return {1}