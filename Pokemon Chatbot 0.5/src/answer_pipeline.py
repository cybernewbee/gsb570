from src.query_extractor import extract_query_fields
from src.google_api import search_walkthrough
from src.pokeapi import get_pokemon_details
from src.claude_writer import generate_walkthrough_article
from langdetect import detect
from src.reverse_lookup import reverse_lookup_pokemon_name




def answer_query(user_input: str) -> dict:
    """
    Master function that:
    1. Extracts structured fields from a user prompt
    2. Searches Google for walkthroughs
    3. Fetches Pokémon spec data from PokéAPI (if valid)
    Returns a combined dict.
    """
    # Step 1: Extract game, intent, and (maybe) Pokémon
    fields = extract_query_fields(user_input)
    if "error" in fields:
        return {"error": f"Keyword extraction failed: {fields['error']}"}

    game = fields.get("game")
    pokemon = fields.get("pokemon")
    intent = fields.get("intent")

    # Step 2: Search walkthroughs using game + intent
    walkthroughs = []
    walkthrough_article = ""

    # Only perform search if game or intent is present
    if game or intent:
        try:
            walkthroughs = search_walkthrough(game or "", intent or "")
        except Exception as e:
            print(f"[WARN] Google search failed: {e}")
            walkthroughs = []

        if walkthroughs:
            try:
                walkthrough_article = generate_walkthrough_article(user_input, walkthroughs)
            except Exception as e:
                walkthrough_article = f"Failed to generate article: {e}"

   # Step 3: Get Pokémon info (only if pokemon is valid and not 'none')
    pokemon_info = {}

    if pokemon and pokemon.lower() != "none":
        # Detect language of the input name
        try:
            lang = detect(pokemon)
            lang_map = {
                "zh-cn": "zh-Hans",
                "zh-tw": "zh-Hant",
                "ja": "ja"
            }
            lang_code = lang_map.get(lang)

            # If it's non-English, attempt reverse lookup
            if lang_code:
                canonical = reverse_lookup_pokemon_name(pokemon, lang_code=lang_code)
                if canonical:
                    pokemon = canonical.lower()

        except Exception as e:
            print(f"[WARN] Language detection failed: {e}")

        # Now fetch from PokéAPI
        try:
            pokemon_info = get_pokemon_details(pokemon)
        except Exception as e:
            pokemon_info = {"error": f"Failed to fetch Pokémon info for {pokemon}: {e}"}
    else:
        pokemon_info = {"error": "No specific Pokémon mentioned in the question."}



    # Step 4: Return combined results
    return {
    "query_fields": fields,
    "walkthrough_results": walkthroughs,
    "walkthrough_article": walkthrough_article,
    "pokemon_info": pokemon_info
    }


