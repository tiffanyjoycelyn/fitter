import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect('user_data.db', check_same_thread=False)
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            username TEXT PRIMARY KEY,
            weight REAL,
            height REAL,
            lifestyle TEXT,
            bmi REAL,
            calories_per_day REAL,
            protein_per_day REAL,
            carbs_per_day REAL,
            fat_per_day REAL,
            bmi_classification TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp TEXT,
            predicted_class TEXT,
            servings INTEGER,
            calories REAL,
            protein REAL,
            carbohydrates REAL,
            fat REAL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    conn.commit()

def save_profile(conn, profile_data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO profiles (username, weight, height, lifestyle, bmi, calories_per_day, protein_per_day, carbs_per_day, fat_per_day, bmi_classification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile_data['username'], 
        profile_data['weight'], 
        profile_data['height'], 
        profile_data['lifestyle'], 
        profile_data['bmi'], 
        profile_data['calories'], 
        profile_data['protein'], 
        profile_data['carbs'], 
        profile_data['fat'],
        profile_data['bmi_classification'],
    ))
    conn.commit()
    print(f"Saved profile for {profile_data['username']}")

def load_profile(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT weight, height, lifestyle, bmi, calories_per_day, protein_per_day, carbs_per_day, fat_per_day, bmi_classification FROM profiles WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        profile = {
            'username': username,
            'weight': result[0],
            'height': result[1],
            'lifestyle': result[2],
            'bmi': result[3],
            'calories': result[4],
            'protein': result[5],
            'carbs': result[6],
            'fat': result[7],
            'bmi_classification': result[8]
        }
        print(f"Loaded profile for {username}: {profile}")
        return profile
    print(f"No profile found for {username}")
    return None

def save_prediction_log_db(conn, log_entry):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prediction_logs (username, timestamp, predicted_class, servings, calories, protein, carbohydrates, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log_entry['username'],
        log_entry['timestamp'],
        log_entry['predicted_class'],
        log_entry['servings'],
        log_entry['calories'],
        log_entry['protein'],
        log_entry['carbohydrates'],
        log_entry['fat']
    ))
    conn.commit()
    print(f"Saved prediction log for {log_entry['username']} at {log_entry['timestamp']}")

def calculate_remaining_nutrition(conn, username, profile_data):
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT SUM(calories), SUM(protein), SUM(carbohydrates), SUM(fat)
        FROM prediction_logs
        WHERE username = ? AND DATE(timestamp) = ?
    """, (username, today))
    
    result = cursor.fetchone()
    
    if result:
        consumed_calories, consumed_protein, consumed_carbs, consumed_fat = result
        if consumed_calories is None:  # Handle case where there are no entries for today
            consumed_calories = 0
        if consumed_protein is None:
            consumed_protein = 0
        if consumed_carbs is None:
            consumed_carbs = 0
        if consumed_fat is None:
            consumed_fat = 0
    else:
        consumed_calories = 0
        consumed_protein = 0
        consumed_carbs = 0
        consumed_fat = 0

    remaining_calories = profile_data['calories'] - consumed_calories
    remaining_protein = profile_data['protein'] - consumed_protein
    remaining_carbs = profile_data['carbs'] - consumed_carbs
    remaining_fat = profile_data['fat'] - consumed_fat

    return remaining_calories, remaining_protein, remaining_carbs, remaining_fat

def recreate_profiles_table():
    conn = sqlite3.connect('user_data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS profiles')
    cursor.execute('''
        CREATE TABLE profiles (
            username TEXT PRIMARY KEY,
            weight REAL,
            height REAL,
            lifestyle TEXT,
            bmi REAL,
            calories_per_day REAL,
            protein_per_day REAL,
            carbs_per_day REAL,
            fat_per_day REAL,
            bmi_classification TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

recreate_profiles_table()
