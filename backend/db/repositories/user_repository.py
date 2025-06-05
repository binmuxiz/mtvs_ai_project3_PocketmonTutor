import logging
import json
from db import get_connection

def get_user_by_id(user_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE user_id = ?", (user_id, ))
    row = cur.fetchone()
    conn.close()
    return row


from models import UserCreate

def create_user(data: UserCreate):
    conn = get_connection()

    try :
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (user_id, name)
            VALUES (?, ?)
        """, (
            data.user_id,
            data.name
        ))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise 

    finally:
        conn.close()
