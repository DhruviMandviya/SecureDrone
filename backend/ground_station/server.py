from fastapi import FastAPI

from backend.ground_station.routes import (
    router
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SecureDrone Ground Control Station",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


