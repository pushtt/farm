# This file is the entry point for Vercel
import sys
from pathlib import Path

# Add the fastapi directory to the Python path so we can import from it
fastapi_path = Path(__file__).parent / "fastapi"
sys.path.insert(0, str(fastapi_path))

# Import the app object from the main.py file in the fastapi directory
from main import app