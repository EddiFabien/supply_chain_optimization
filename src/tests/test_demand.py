import pytest
from fastapi.testclient import TestClient
from src.app.main import app
import os
from pathlib import Path
import pandas as pd

# Create a test client instance
client = TestClient(app)

def test_demand_forecast_success():
    """
    Test successful demand forecast request
    """
    test_data = {
        "year": 2011,
        "month": 8,
        "country": "Australia",
        "product_description": "BLUE_DINER"
    }

def test_demand_forecast_invalid_country():
    """
    Test invalid country
    """
    test_data = {
        "year": 2011,
        "month": 8,
        "country": "InvalidCountry",
        "product_description": "BLUE_DINER"
    }
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 404
    assert "No forecast model found" in response.json()['detail']

def test_demand_forecast_invalid_product():
    """
    Test invalid product
    """
    test_data = {
        "year": 2011,
        "month": 8,
        "country": "Australia",
        "product_description": "INVALID_PRODUCT"
    }
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 404
    assert "No forecast model found" in response.json()['detail']

def test_demand_forecast_invalid_time():
    """
    Test invalid time period
    """
    test_data = {
        "year": 2011,
        "month": 13,  # Invalid month
        "country": "Australia",
        "product_description": "BLUE_DINER"
    }
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 400
    assert "Month must be between 1 and 12" in response.json()['detail']

def test_demand_forecast_missing_fields():
    """
    Test missing required fields
    """
    test_data = {
        "year": 2011,
        "month": 8
    }
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 422
    assert "country" in response.json()['detail'][0]['loc']
    assert "product_description" in response.json()['detail'][1]['loc']

def test_demand_forecast_invalid_input_type():
    """
    Test invalid input types
    """
    test_data = {
        "year": "not_a_number",
        "month": "also_not_a_number",
        "country": "Australia",
        "product_description": "BLUE_DINER"
    }
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 422
    assert "year" in response.json()['detail'][0]['loc']
    assert "month" in response.json()['detail'][1]['loc']
    
    # Test the endpoint
    response = client.post("/forecast/demand", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "forecast_quantity" in data
    assert "confidence_interval_lower" in data
    assert "confidence_interval_upper" in data
    
    # Verify specific values
    assert isinstance(data["forecast_quantity"], (int, float))
    assert isinstance(data["confidence_interval_lower"], (int, float))
    assert isinstance(data["confidence_interval_upper"], (int, float))
    
    # Verify confidence interval
    assert data["confidence_interval_lower"] <= data["forecast_quantity"] <= data["confidence_interval_upper"]

def test_demand_forecast_invalid_country():
    """
    Test demand forecast with invalid country
    """
    test_data = {
        "year": 2025,
        "month": 5,
        "country": "InvalidCountry",
        "product_description": "BLUE_HARMO"
    }
    
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "No forecast model found" in response.json()["detail"]

def test_demand_forecast_invalid_product():
    """
    Test demand forecast with invalid product
    """
    test_data = {
        "year": 2025,
        "month": 5,
        "country": "Australia",
        "product_description": "INVALID_PRODUCT"
    }
    
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "No forecast model found" in response.json()["detail"]

def test_demand_forecast_invalid_time():
    """
    Test demand forecast with invalid time period
    """
    test_data = {
        "year": 2025,
        "month": 13,  # Invalid month
        "country": "Australia",
        "product_description": "BLUE_HARMO"
    }
    
    # Create mock data with only month 5
    mock_data = {
        'Year': [2025],
        'Month': [5],
        'Forecast': [150.5],
        'Lower CI': [140.5],
        'Upper CI': [160.5]
    }
    
    # Create mock file in the actual models directory
    models_dir = Path("src") / "models" / "demand_predictions"
    file_path = models_dir / f"{test_data['country'].upper()}_{test_data['product_description'].upper().replace(' ', '_')}_forecast.csv"
    
    # Ensure the directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.DataFrame(mock_data)
    df.to_csv(file_path, index=False)
    
    try:
        response = client.post("/api/v1/forecast/demand", json=test_data)
        assert response.status_code == 400
        assert "detail" in response.json()
        assert "Month must be between 1 and 12" in response.json()["detail"]
        
    finally:
        # Clean up
        if file_path.exists():
            file_path.unlink()
            # Remove empty directories
            try:
                file_path.parent.rmdir()
                file_path.parent.parent.rmdir()
                file_path.parent.parent.parent.rmdir()
            except OSError:
                pass

def test_demand_forecast_missing_fields():
    """
    Test demand forecast with missing required fields
    """
    test_data = {
        "year": 2025,
        "month": 5
    }
    
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 422  # Unprocessable entity
    assert "detail" in response.json()
    assert len(response.json()["detail"]) > 0

def test_demand_forecast_invalid_input_type():
    """
    Test demand forecast with invalid input types
    """
    test_data = {
        "year": "not_a_number",  # Invalid type for year
        "month": 5,
        "country": "Australia",
        "product_description": "BLUE_HARMO"
    }
    
    response = client.post("/api/v1/forecast/demand", json=test_data)
    assert response.status_code == 422  # Unprocessable entity
    assert "detail" in response.json()
    assert len(response.json()["detail"]) > 0
