import os, requests
from functools import lru_cache

# Load environment variables from .env file
API_KEY = os.getenv('TMDB_API_KEY')

# Base Url for TMDB API
BASE_URL = "https://api.themoviedb.org/3"


# Method to make the requests
def make_request(endpoint):
    try:
        url = f"{BASE_URL}/{endpoint}"
        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {endpoint}: {e}")
        return None


@lru_cache(maxsize=1)
def get_movie_genres():
    
    """
    Fetches the list of movie genres from the TMDB API.

    Returns:
        list: A list of dictionaries containing genre information.
    """
    endpoint = "genre/movie/list"
    response_data = make_request(endpoint)

    if not response_data:
        return []
    return response_data.get("genres", [])


@lru_cache(maxsize=1)
def get_all_languages():
    """
    Fetches the list of all the available languages from the TMDB API.

    Returns:
        list: A list of dictionaries containing languages information.
    """
    endpoint = "configuration/languages"
    response_data = make_request(endpoint)

    if not response_data:
        return []
    return response_data
        