export interface PokemonData {
  name: string;
  no: string;
  pokemon_type: string[];
  description: string;
  match: {
    personality: string;
    hobby: string;
    color: string;
    mood: string;
    type: string;
  };
  image: string;
}

