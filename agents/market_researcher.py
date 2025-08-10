import pandas as pd
import time
from datetime import datetime
from database.queries import update_market_prices
from config import MARKET_DATA

# Load market data
market_df = pd.read_csv(MARKET_DATA)

def analyze_market(market_data_list):
    try:
        top_crops = market_df.sort_values("Market_Price_per_ton", ascending=False).head(5)
        
        market_data_list.clear()
        for _, row in top_crops.iterrows():
            market_data_list.append({
                "product": row["Product"],
                "price": row["Market_Price_per_ton"],
                # Remove "demand" if column doesn't exist
                "demand": row.get("Demand_Level", "Medium")  # .get() prevents KeyError
            })
        
        # Update database with market prices
        update_market_prices(market_data_list)
        
    except Exception as e:
        print(f"Market research error: {e}")

def start_market_agent(market_data_list, interval=60):
    while True:
        analyze_market(market_data_list)
        time.sleep(interval)