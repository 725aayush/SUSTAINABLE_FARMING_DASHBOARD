import pandas as pd
from config import FARMER_DATA, MARKET_DATA

def load_farmer_data():
    try:
        return pd.read_csv(FARMER_DATA)
    except Exception as e:
        print(f"Error loading farmer data: {e}")
        return None

def load_market_data():
    try:
        return pd.read_csv(MARKET_DATA)
    except Exception as e:
        print(f"Error loading market data: {e}")
        return None

def get_initial_data():
    return {
        "farmer_data": load_farmer_data(),
        "market_data": load_market_data()
    }