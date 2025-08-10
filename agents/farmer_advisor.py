import ollama
import pandas as pd
import time
from datetime import datetime
from database.queries import save_recommendation
from config import FARMER_DATA

# Load data
farmer_data = pd.read_csv(FARMER_DATA)

def generate_recommendations(farmer_name, recommendations_list):
    try:
        best_crop_row = farmer_data.sort_values("Sustainability_Score", ascending=False).iloc[0]
        
        # Prepare query for LLM
        user_input = f"""
        Suggest 5 sustainable crops for {farmer_name} based on:
        - Soil pH: {best_crop_row["Soil_pH"]}
        - Soil Moisture: {best_crop_row["Soil_Moisture"]}
        - Temperature: {best_crop_row["Temperature_C"]}°C
        - Rainfall: {best_crop_row["Rainfall_mm"]}mm
        """
        
        # Get AI suggestion
        try:
            response = ollama.chat(
                model="tinyllama", 
                messages=[{"role": "user", "content": user_input}]
            )
            ai_suggestion = response["message"]["content"]
        except Exception as e:
            print(f"Ollama error: {e}")
            ai_suggestion = "Default crops: Wheat, Rice, Maize, Barley, Millet"
        
        # Save to database
        rec_id = save_recommendation(
            farmer_name=farmer_name,
            suggestion=ai_suggestion,
            soil_ph=best_crop_row["Soil_pH"],
            soil_moisture=best_crop_row["Soil_Moisture"],
            temperature=best_crop_row["Temperature_C"],
            rainfall=best_crop_row["Rainfall_mm"],
            score=best_crop_row["Sustainability_Score"]
        )
        
        # Update global list
        recommendations_list.clear()
        recommendations_list.append({
            "id": rec_id,
            "farmer": farmer_name,
            "suggestion": ai_suggestion,
            "score": best_crop_row["Sustainability_Score"],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Farmer advisor error: {e}")

def start_farmer_agent(recommendations_list, interval=30):
    while True:
        if recommendations_list:  # Only run if we have active farmer
            generate_recommendations(recommendations_list[-1]["farmer"], recommendations_list)
        time.sleep(interval)