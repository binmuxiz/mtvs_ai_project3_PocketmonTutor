import logging
import json
from db import get_connection

from models import Pokemon


def get_pokemon_by_user_id(user_id: str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
                SELECT user_id, name, no, pokemon_type, description, match, image, model_file_path 
                FROM user_pokemons 
                    WHERE user_id = ?
                    """, (user_id, ))
        row = cur.fetchone()
        return row

    except Exception as e:
        raise
    finally:
        conn.close()


def create_pokemon(pokemon: Pokemon):
    conn = get_connection()
    print(pokemon.model_file_path)
    try:
        cur = conn.cursor()
        cur.execute("""
                INSERT INTO user_pokemons (
                    user_id, name, no, pokemon_type, description, match, image, model_file_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                    pokemon.user_id,
                    pokemon.name.strip(),
                    int(pokemon.no),
                    ",".join(pokemon.pokemon_type),
                    pokemon.description,
                    json.dumps(pokemon.match, ensure_ascii=False),  # match는 JSON으로 직렬화
                    pokemon.image,
                    pokemon.model_file_path
                ))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise 

    finally:
        conn.close()

