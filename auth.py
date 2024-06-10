import bcrypt
import sqlite3
import streamlit as st
import time

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

def login_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    return False

def register_user(conn, username, password):
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")

def logout():
    st.session_state["login_status"] = False
    st.session_state.pop("username", None)
    st.experimental_rerun()

def splash_screen():
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            padding-top: 0px;
            padding-right: 0px;
            padding-left: 0px;
            padding-bottom: 0px;
        }}
        .splash-screen {{
            background-color: black;
            color: white;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 9999;
        }}
        .splash-screen h1 {{
            font-size: 3em;
        }}
        .splash-screen img {{
            width: 200px;
        }}
        .splash-screen p {{
            font-size: 1.2em;
        }}
        </style>
        <div class="splash-screen">
            <img src="data:image/png;base64,{st.session_state["logo_base64"]}" alt="fitter logo">
            <h1>Welcome to fitter!</h1>
            <p>Track Your Nutrition</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)
    st.session_state["show_splash"] = False
    st.experimental_rerun()
