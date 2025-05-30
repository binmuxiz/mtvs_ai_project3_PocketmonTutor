import sqlite3

DB_NAME = "pokemon-tutor.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  # 외래키 강제 활성화
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users 테이블 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            personality TEXT,
            hobby TEXT,
            color TEXT,
            mood TEXT,
            type TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_pokemons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT,
            file_path TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)  ON DELETE CASCADE
        );
    """)


    conn.commit()
    conn.close()

