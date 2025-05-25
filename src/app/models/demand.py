from pydantic import BaseModel

class DemandForecastRequest(BaseModel):
    year: int
    month: int
    country: str
    product_description: str

class DemandForecastResponse(BaseModel):
    forecast_quantity: float
    confidence_interval_lower: float
    confidence_interval_upper: float
