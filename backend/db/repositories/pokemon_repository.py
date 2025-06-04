import logging
import json
from db import get_connection

from models import Pokemon


def create_pokemon(pokemon: Pokemon):
    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("""
                INSERT INTO user_pokemons (
                    user_id, name, no, pokemon_type, description, match_json, image, model_file_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
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

    except Exception as e:
        conn.rollback()
        raise 

    finally:
        conn.close()


def update_