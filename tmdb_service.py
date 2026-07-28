import os, requests
from functools import lru_cache

# Load environment variables from .env file
API_KEY = os.getenv('TMDB_API_KEY')

# Base Url for TMDB API
BASE_URL = "https://api.themoviedb.org/3"


# Method to make the API requests
def make_request(endpoint, params=None):
    try:
        url = f"{BASE_URL}/{endpoint}"

        default_params = {
            "api_key": API_KEY,
            "language": "en-US",
        }

        if params:
            default_params.update(params)

        response = requests.get(url, params=default_params, timeout=10)

        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {endpoint}: {e}")
        return None


@lru_cache(maxsize=1)
def get_movie_genres():
    endpoint = "genre/movie/list"
    response_data = make_request(endpoint)

    return response_data.get("genres", [])


@lru_cache(maxsize=1)
def get_tv_genres():
    endpoint = "genre/tv/list"
    response_data = make_request(endpoint)

    return response_data.get("genres", [])


@lru_cache(maxsize=1)
def get_all_languages():
    endpoint = "configuration/languages"
    response_data = make_request(endpoint)

    if not response_data:
        return []
    return response_data


def discover_media(params, watch_type="movie", page=1):
    endpoint = f"discover/{watch_type}"

    params = params.copy()
    params["page"] = page

    response_data = make_request(endpoint, params)
    
    return response_data


def get_movie_tv_details(tmdb_id, watch_type="movie"):
    params = {
    "append_to_response": "credits,videos,watch/providers,images",
    "include_image_language": "en,null"
    }

    response_data = make_request(f"{watch_type}/{tmdb_id}", params)
    
    if not response_data:
            return None
    return response_data
