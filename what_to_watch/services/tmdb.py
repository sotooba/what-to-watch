import hashlib
import json

import requests
from flask import current_app

from ..extensions import cache


BASE_URL = "https://api.themoviedb.org/3"


def _ttl(name):
    return current_app.config["TMDB_CACHE_TTLS"][name]


def _cache_key(namespace, value):
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    return f"tmdb:{namespace}:{digest}"


def _cached_response(namespace, value, timeout, loader):
    """Cache only successful TMDB payloads; failures remain retryable."""
    key = _cache_key(namespace, value)
    cached = cache.get(key)
    if cached is not None:
        return cached

    payload = loader()
    if payload is not None:
        cache.set(key, payload, timeout=timeout)
    return payload


def make_request(endpoint, params=None):
    api_key = current_app.config.get("TMDB_API_KEY")
    if not api_key:
        current_app.logger.error("TMDB_API_KEY is not configured")
        return None

    request_params = {"api_key": api_key, "language": "en-US"}
    if params:
        request_params.update(params)

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=request_params, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        current_app.logger.warning("TMDB request failed for %s: %s", endpoint, error)
        return None


def _get(endpoint, params=None, *, namespace, timeout):
    request_data = {"endpoint": endpoint, "params": params or {}}
    return _cached_response(
        namespace,
        request_data,
        timeout,
        lambda: make_request(endpoint, params),
    )


def get_movie_genres():
    payload = _get("genre/movie/list", namespace="movie-genres", timeout=_ttl("configuration"))
    return (payload or {}).get("genres", [])


def get_tv_genres():
    payload = _get("genre/tv/list", namespace="tv-genres", timeout=_ttl("configuration"))
    return (payload or {}).get("genres", [])


def get_all_languages():
    payload = _get("configuration/languages", namespace="languages", timeout=_ttl("configuration"))
    return payload or []


def discover_media(params, watch_type="movie", page=1):
    request_params = {**params, "page": page}
    return _get(
        f"discover/{watch_type}",
        request_params,
        namespace="discover",
        timeout=_ttl("discover"),
    )


def get_movie_tv_details(tmdb_id, watch_type="movie"):
    params = {
        "append_to_response": "credits,videos,watch/providers,images",
        "include_image_language": "en,null",
    }
    return _get(
        f"{watch_type}/{tmdb_id}",
        params,
        namespace="details",
        timeout=_ttl("details"),
    )


def get_related_recommendations(tmdb_id, watch_type="movie"):
    endpoints = [
        f"{watch_type}/{tmdb_id}/recommendations",
        f"{watch_type}/{tmdb_id}/similar",
    ]

    for endpoint in endpoints:
        payload = _get(endpoint, namespace="related", timeout=_ttl("details"))
        results = (payload or {}).get("results", [])
        if results:
            return results[:10]

    return []


def get_trending(media_type, time_window):
    payload = _get(
        f"trending/{media_type}/{time_window}",
        namespace="trending",
        timeout=_ttl("trending"),
    )
    return (payload or {}).get("results", [])


def get_popular(media_type):
    payload = _get(
        f"{media_type}/popular",
        namespace="popular",
        timeout=_ttl("popular"),
    )
    return (payload or {}).get("results", [])


def get_search_results(query):
    payload = _get(
        "search/multi",
        {"query": query},
        namespace="search",
        timeout=_ttl("search"),
    )
    return (payload or {}).get("results", [])
