
import sqlite3
import json

def get_all_records():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_requests")
    records = cursor.fetchall()
    conn.close()
    return records


def update_record(record_id, new_location, new_start_date, new_end_date, new_temperature_data):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE weather_requests
        SET location = ?, start_date = ?, end_date = ?, temperature_data = ?
        WHERE id = ?
    """, (new_location, new_start_date, new_end_date, json.dumps(new_temperature_data), record_id))
    conn.commit()
    conn.close()


def delete_record(record_id):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather_requests WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def init_db():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            temperature_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()



def save_weather_data(location, start_date, end_date, temperature_data):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather_requests (location, start_date, end_date, temperature_data)
        VALUES (?, ?, ?, ?)
    """, (location, start_date, end_date, json.dumps(temperature_data)))
    conn.commit()
    conn.close()