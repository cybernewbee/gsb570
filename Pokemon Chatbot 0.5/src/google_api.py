import os
import requests
from dotenv import load_dotenv

load_dotenv('/Users/marvinlee/Documents/vs_code/gsb_570/Pokemon Chatbot/config/.env')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CSE_ID")

def search_walkthrough(game_name: str, topic: str, num_results: int = 5) -> list:
    """
    Search Google for game walkthroughs using Programmable Search Engine.
    Returns a list of dictionaries with title, snippet, and link.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CX:
        raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID in environment variables.")

    query = f"{game_name} {topic} site:gamefaqs.gamespot.com OR site:ign.com OR site:bulbapedia.bulbagarden.net"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": num_results,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Google API error: {response.status_code} - {response.text}")

    results = response.json().get("items", [])
    return [
        {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        }
        for item in results
    ]





