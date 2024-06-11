import sqlite3

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
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    conn.commit()

def save_profile(conn, profile_data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO profiles (username, weight, height, lifestyle, bmi, calories_per_day, protein_per_day, carbs_per_day, fat_per_day)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile_data['name'], 
        profile_data['weight'], 
        profile_data['height'], 
        profile_data['lifestyle'], 
        profile_data['bmi'], 
        profile_data['calories'], 
        profile_data['protein'], 
        profile_data['carbs'], 
        profile_data['fat']
    ))
    conn.commit()

def load_profile(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT weight, height, lifestyle,bmi, calories_per_day, protein_per_day, carbs_per_day, fat_per_day FROM profiles WHERE username = ?', (username,))
    result = cursor.fetchone()
    return result
