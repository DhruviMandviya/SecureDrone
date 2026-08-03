from fastapi import FastAPI

from backend.ground_station.routes import (
    router
)

app = FastAPI(
    title="SecureDrone Ground Control Station",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def home():

    return {
        "message": "SecureDrone Ground Control Station",
        "status": "Running"
    }


@app.get("/health")
async def health():

    return {
        "status": "Healthy"
    }


@app.get("/status")
async def status():

    return {
        "ground_station": "online"
    }