import sys
import os

# Add the 'backend' directory to sys.path to allow importing from it
# 'api' directory is at project root, 'backend' is also at project root
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Import the FastAPI app instance from backend/main.py
from main import app
