from db import get_connection


# ==================================== DB 초기화 ==================================== 

def init_db():
    conn = get_connection()
    cur = conn.cursor()

# 유저 테이블 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        );
    """)

# 유저 포켓몬 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_pokemons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL, 
            name TEXT,
            no INTEGER,
            pokemon_type TEXT,
            description TEXT,
            match_json TEXT,
            image TEXT,
            model_file_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

# 투두 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            complete INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)


# 챗 히스토리 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            sender TEXT CHECK(sender IN ('user', 'ai')) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
