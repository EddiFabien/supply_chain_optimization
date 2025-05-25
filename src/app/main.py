from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os
from pathlib import Path
from .routes.demand import router as demand_router

app = FastAPI(
    title="Supply Chain Optimization API",
    description="API for supply chain optimization with demand forecasting",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(demand_router)

# Define the input model
class DemandForecastRequest(BaseModel):
    year: int
    month: int
    country: str
    product_description: str

# Define the response model
class DemandForecastResponse(BaseModel):
    forecast_quantity: float
    confidence_interval_lower: float
    confidence_interval_upper: float

@app.get("/")
async def root():
    return {"message": "Welcome to Supply Chain Optimization API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
