from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
import pandas as pd
from pathlib import Path
from ..models.demand import DemandForecastRequest, DemandForecastResponse
from ..config import MODELS_DIR
import os

router = APIRouter(prefix="/api/v1")

@router.post("/forecast/demand", response_model=DemandForecastResponse)
async def get_demand_forecast(request: DemandForecastRequest):
    print(f"Current working directory: {os.getcwd()}")
    print(f"MODELS_DIR: {MODELS_DIR}")
    print(f"File exists: {MODELS_DIR.exists()}")
    print(f"Request data: {request.model_dump()}")
    try:
        # Validate input data
        if request.month < 1 or request.month > 12:
            raise HTTPException(
                status_code=400,
                detail="Month must be between 1 and 12"
            )
        
        # Convert country and product description to match file naming convention
        country = request.country.upper()
        product_description = request.product_description.upper().replace(" ", "_")
        print(f"Converted country: {country}")
        print(f"Converted product: {product_description}")
        
        # Construct the expected filename
        filename = f"{country}_{product_description}_forecast.csv"
        file_path = MODELS_DIR / filename
        print(f"Expected file path: {file_path}")
        print(f"File exists: {file_path.is_file()}")
        
        # Ensure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not file_path.is_file():
            raise HTTPException(
                status_code=404,
                detail=f"No forecast model found for country: {request.country} and product: {request.product_description}"
            )
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            print(f"Successfully read CSV file with columns: {list(df.columns)}")
            
            # Map the column names from the CSV to our expected names
            column_map = {
                'Date': 'Date',
                'Forecasted_Quantity': 'Forecast',
                'Lower_Bound': 'Lower CI',
                'Upper_Bound': 'Upper CI',
                'Actual': 'Actual'
            }
            
            # Rename columns to match our expected names
            df = df.rename(columns=column_map)
            
            # Extract year and month from Date column if it exists
            if 'Date' in df.columns:
                df['Year'] = pd.to_datetime(df['Date']).dt.year
                df['Month'] = pd.to_datetime(df['Date']).dt.month
            
            # Get the forecast for the requested month
            forecast_data = df[(df['Year'] == request.year) & (df['Month'] == request.month)]
            if forecast_data.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"No forecast data found for year: {request.year} and month: {request.month}"
                )
                
            # Prepare the response
            response_data = {
                "year": request.year,
                "month": request.month,
                "country": request.country,
                "product_description": request.product_description,
                "forecast": float(forecast_data['Forecast'].iloc[0]),
                "lower_ci": float(forecast_data['Lower CI'].iloc[0]),
                "upper_ci": float(forecast_data['Upper CI'].iloc[0])
            }
            return DemandForecastResponse(
                forecast_quantity=response_data['forecast'],
                confidence_interval_lower=response_data['lower_ci'],
                confidence_interval_upper=response_data['upper_ci']
            )
            
        except Exception as e:
            print(f"Error reading or processing CSV file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Forecast file is missing required columns"
            )
        
        # Filter by year and month
        filtered_df = df[(df['Year'] == request.year) & (df['Month'] == request.month)]
        
        if filtered_df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No forecast available for year: {request.year} and month: {request.month}"
            )
            
        # Get the forecast values
        forecast = filtered_df.iloc[0]
        return DemandForecastResponse(
            forecast_quantity=forecast['Forecast'],
            confidence_interval_lower=forecast['Lower CI'],
            confidence_interval_upper=forecast['Upper CI']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
