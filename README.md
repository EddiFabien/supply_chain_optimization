# Supply Chain Optimization API

A FastAPI-based API service for supply chain optimization with demand forecasting capabilities.

## Project Overview

This project provides a RESTful API service for supply chain optimization, focusing on demand forecasting using ARIMA models. The API allows users to get demand forecasts for specific products in different countries based on historical data.

## Features

- Demand forecasting by context (country, product, time period)
- RESTful API endpoints
- Input validation using Pydantic models
- Error handling and proper HTTP responses
- Auto-generated API documentation (Swagger UI)
- Modular code structure
- Type hints and code quality checks

## Project Structure

```
Supply_chain_optimization/
├── dataset/                  
│   ├── data_processed/                       # processed data
│   └── data_raw/                             # raw data
├── src/                                      # Source code
│   ├── app/                                  # FastAPI application code
│   ├── data/                                 # preprocessed data
│   ├── mapreduce/                            # mapreduce codes
│   ├── models/                               # Trained ARIMA models  
│   ├── supply_chain_optimization/            # supply chain optimization codes for all models
│   ├── tests/                                # Test codes
│   │   └── test_inputs.json                  # Valid input combinations for testing
├── .gitignore                                # Git ignore file
├── requirements.txt                          # Project dependencies
└── README.md                                 # Project documentation
```

## Valid Input Combinations

The project includes a [test_inputs.json](cci:7://file:///c:/Users/eddi/OneDrive/Bureau/Supply_chain_optimization/src/tests/test_inputs.json:0:0-0:0) file that lists all valid combinations of countries and products. This file can be used to:

1. Validate input data before making API requests
2. Generate test cases for automated testing
3. Understand the available product offerings per country

The file contains:
- List of all valid countries
- Country-specific product lists
- Valid time range (years and months)

Example usage:
```python
import json

# Load test inputs
with open('src/tests/test_inputs.json', 'r') as f:
    test_inputs = json.load(f)

# Get valid products for a specific country
australian_products = test_inputs['products']['Australia']

# Get valid time range
valid_years = range(test_inputs['time_range']['start_year'], test_inputs['time_range']['end_year'] + 1)
valid_months = test_inputs['time_range']['months']
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

```bash
# Run from the project root directory
cd src
PYTHONPATH=".." uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Base URL

`http://localhost:8000`

### Available Endpoints

#### 1. Demand Forecast

- **Endpoint**: `/api/v1/forecast/demand`
- **Method**: POST
- **Description**: Get demand forecast for a specific product in a country
- **Request Body**:
  ```json
  {
    "year": 2025,
    "month": 5,
    "country": "Australia",
    "product_description": "BLUE_DINER"
  }
  ```
- **Response**:
  ```json
  {
    "forecast_quantity": 0.0,
    "confidence_interval_lower": -0.5577179321476949,
    "confidence_interval_upper": 0.5577179321476949
  }
  ```

### API Documentation

The API provides auto-generated Swagger UI documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API uses HTTP status codes to indicate different types of errors:

- 404: No forecast model found for the specified country and product
- 404: No forecast available for the specified time period
- 422: Invalid input data (missing required fields or invalid types)
- 500: Internal server error

## Testing

To run the test suite:

```bash
python -m pytest tests/ -v
```

The test suite includes:
- Successful demand forecast test
- Invalid country test
- Invalid product test
- Invalid time period test
- Missing fields test
- Invalid input type test

## Dependencies

The project uses the following main dependencies:

- FastAPI: Modern, fast (high-performance) web framework
- Uvicorn: ASGI server implementation
- Pandas: Data manipulation and analysis
- Pydantic: Data validation and settings management
- pytest: Testing framework
- bottleneck: Fast NumPy array functions
- numpy: Numerical computing
- scipy: Scientific computing