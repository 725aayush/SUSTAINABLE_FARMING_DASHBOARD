from flask import Flask, render_template, request, jsonify, send_file
from agents.weather_agent import update_weather
from agents.farmer_advisor import generate_recommendations
from database.db import get_db
from utils.visualization import create_profitability_chart
import threading
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Global variables (in production, use Redis or database)
weather_data = {"temp": 0, "condition": "Unknown", "humidity": 0, "wind": 0}
recommendations = []
market_data = []
current_farmer = ""
current_city = app.config['DEFAULT_CITY']

@app.route('/')
def index():
    return render_template(
        'index.html',
        weather=weather_data,
        recommendations=recommendations,
        market_data=market_data,
        current_farmer=current_farmer,
        current_city=current_city,
        chart_image=create_profitability_chart(market_data)  # ✅ added
    )

@app.route('/submit_farmer', methods=['POST'])
def submit_farmer():
    global current_farmer, current_city

    data = request.get_json()
    farmer_name = data.get('name', '').strip()
    city = data.get('city', app.config['DEFAULT_CITY']).strip()

    if not farmer_name:
        return jsonify({"error": "Farmer name is required"}), 400

    current_farmer = farmer_name
    current_city = city

    # Update weather immediately
    weather_thread = threading.Thread(target=update_weather, args=(city, weather_data))
    weather_thread.start()

    # Generate recommendations
    rec_thread = threading.Thread(target=generate_recommendations, args=(farmer_name, recommendations))
    rec_thread.start()

    return jsonify({"message": "Processing recommendations..."})

@app.route('/get_updates')
def get_updates():
    print("Recommendations:", recommendations)
    return jsonify({
        "weather": weather_data,
        "recommendations": recommendations,
        "market_data": market_data
    })

@app.route('/get_market_chart')
def get_market_chart():
    return jsonify({
        "chart": create_profitability_chart(market_data)
    })

@app.route('/export_recommendations')
def export_recommendations():
    import pandas as pd
    from io import BytesIO
    from database.queries import get_all_recommendations

    data = get_all_recommendations()
    if not data:
        return "No data to export", 404

    df = pd.DataFrame(data, columns=[
        'ID', 'Farmer Name', 'Suggested Crops', 'Soil pH', 'Soil Moisture',
        'Temperature (°C)', 'Rainfall (mm)', 'Sustainability Score',
        'Weather Condition', 'Market Price (₹/ton)', 'Timestamp'
    ])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Recommendations')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='farm_recommendations.xlsx'
    )

def run_agents():
    from agents.weather_agent import start_weather_agent
    from agents.farmer_advisor import start_farmer_agent
    from agents.market_researcher import start_market_agent

    weather_thread = threading.Thread(target=start_weather_agent, args=(weather_data,))
    farmer_thread = threading.Thread(target=start_farmer_agent, args=(recommendations,))
    market_thread = threading.Thread(target=start_market_agent, args=(market_data,))

    weather_thread.daemon = True
    farmer_thread.daemon = True
    market_thread.daemon = True

    weather_thread.start()
    farmer_thread.start()
    market_thread.start()

if __name__ == '__main__':
    from database.db import init_db
    init_db()

    run_agents()

    app.run(debug=True)
