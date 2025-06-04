import sqlite3

DB_NAME = "pokemon-tutor.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  # 외래키 강제 활성화
    return conn
