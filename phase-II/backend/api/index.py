import sys
import os

# Add the parent directory to sys.path so Vercel can find main.py and routers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
