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

def save_profile(conn, username, weight, height, lifestyle, bmi, calories, protein, carbs, fat):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO profiles (username, weight, height, lifestyle, bmi, calories_per_day, protein_per_day, carbs_per_day, fat_per_day)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            weight=excluded.weight,
            height=excluded.height,
            lifestyle=excluded.lifestyle,
            bmi=excluded.bmi,
            calories_per_day=excluded.calories_per_day,
            protein_per_day=excluded.protein_per_day,
            carbs_per_day=excluded.carbs_per_day,
            fat_per_day=excluded.fat_per_day
    ''', (username, weight, height, lifestyle, bmi, calories, protein, carbs, fat))
    conn.commit()

def load_profile(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT weight, height, lifestyle FROM profiles WHERE username = ?', (username,))
    result = cursor.fetchone()
    return result
