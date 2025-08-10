import sqlite3
from config import DATABASE
from pathlib import Path

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Path(DATABASE).parent.mkdir(exist_ok=True)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_recommendations (
            id INTEGER PRIMARY KEY,
            farmer_name TEXT,
            suggested_crop TEXT,
            soil_ph REAL,
            soil_moisture REAL,
            temperature REAL,
            rainfall REAL,
            sustainability_score REAL,
            weather_condition TEXT,
            market_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()