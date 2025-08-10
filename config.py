import os
from pathlib import Path

# 1. Base Directory Setup
# This automatically detects your project's root folder
try:
    BASE_DIR = Path(__file__).parent.parent  # Goes up two levels from config.py
except NameError:
    BASE_DIR = Path(os.getcwd())  # Fallback to current directory

# 2. Data Paths (CSV Files)
DATA_DIR = BASE_DIR / "app" / "data"  # Points to sfa/app/data/

FARMER_DATA = DATA_DIR / "farmer_advisor_dataset.csv"
MARKET_DATA = DATA_DIR / "market_researcher_dataset.csv"

# 3. Database Path
DATABASE = BASE_DIR / "app" / "database" / "agriculture_ai.db"

# 4. Weather API
WEATHER_API_KEY = "YOUR_API_KEY"  # Replace with your actual key from weatherapi.com
DEFAULT_CITY = "Bangalore"  # Default location

# 5. Create folders if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATABASE.parent, exist_ok=True)

# 6. Validation (Prints paths for debugging - you can remove later)
"""print("\n[Config Path Verification]")
print(f"Project Root: {BASE_DIR}")
print(f"Farmer Data: {FARMER_DATA} (Exists: {FARMER_DATA.exists()})")
print(f"Market Data: {MARKET_DATA} (Exists: {MARKET_DATA.exists()})")
print(f"Database: {DATABASE}\n")"""