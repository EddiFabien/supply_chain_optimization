import os
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Define paths
MODELS_DIR = ROOT_DIR / "src" / "models" / "demand_predictions"

# For testing purposes
MODELS_DIR = Path(os.getenv('TEST_MODELS_DIR', str(MODELS_DIR)))
