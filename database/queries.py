from database.db import get_db

def save_recommendation(farmer_name, suggestion, soil_ph, soil_moisture, temperature, rainfall, score):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO farmer_recommendations 
            (farmer_name, suggested_crop, soil_ph, soil_moisture, temperature, rainfall, sustainability_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (farmer_name, suggestion, soil_ph, soil_moisture, temperature, rainfall, score))
        
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Database error saving recommendation: {e}")
        return None
    finally:
        conn.close()

def update_market_prices(market_data):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        for item in market_data:
            cursor.execute('''
                UPDATE farmer_recommendations
                SET market_price = ?
                WHERE suggested_crop LIKE ?
            ''', (item["price"], f"%{item['product']}%"))
        
        conn.commit()
    except Exception as e:
        print(f"Database error updating market prices: {e}")
    finally:
        conn.close()

def get_all_recommendations():
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM farmer_recommendations
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Database error fetching recommendations: {e}")
        return []
    finally:
        conn.close()