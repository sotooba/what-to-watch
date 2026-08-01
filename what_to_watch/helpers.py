import hashlib
import json
from pathlib import Path
from random import randint, sample
import pycountry
from flask import current_app

# My methods
from .constants import POPULAR_LANGUAGES, MOVIE_ERA_MAPPING, TV_ERA_MAPPING
from .extensions import cache
from .services.tmdb import discover_media, get_movie_tv_details


def get_popular_languages(all_languages):
    if not all_languages:
        return []

    filtered_languages = []

    for language in all_languages:
        if language.get("iso_639_1") in POPULAR_LANGUAGES:
            filtered_languages.append(language)
    
    return sorted(filtered_languages, key=lambda d: d.get("english_name", ""))


def convert_filters_to_params(filters):
    params = {
        "sort_by": "popularity.desc",
        "include_adult": filters.get("adult", False),
        "vote_average.gte": filters.get("rating") or 7,
    }

    watch_type = filters.get("type")
    language = filters.get("language", "en")
    selected_year = filters.get("year")

    # Genre
    if filters.get("genre"):
        params["with_genres"] = filters["genre"]

    # Language
    if filters.get("language"):
        params["with_original_language"] = filters["language"]

    # Vote count threshold
    if watch_type == "movie":
        params["vote_count.gte"] = 2000 if language == "en" else 300

        if selected_year:
            params.update(MOVIE_ERA_MAPPING.get(selected_year, {}))
        else:
            params["primary_release_date.gte"] = "1980-01-01"

    else:
        params["vote_count.gte"] = 500 if language == "en" else 5

        if selected_year:
            params.update(TV_ERA_MAPPING.get(selected_year, {}))
        else:
            params["first_air_date.gte"] = "1980-01-01"

    return params


def discover_movies_tv(filters, watch_type="movie"):
    params = convert_filters_to_params(filters)

    # First request to determine the number of available pages
    response = discover_media(params, watch_type)
    if not response:
        return None

    total_pages = min(response.get("total_pages", 1), 500)

    # Pick up to 3 unique random pages
    random_pages = sample(
        range(1, total_pages + 1),
        k=min(3, total_pages)
    )

    movies = []

    # Fetch movies from each random page
    for page in random_pages:
        response = discover_media(params, watch_type, page)
        if not response:
            return None
        movies.extend(response.get("results", []))

    # Remove duplicate movies by TMDb ID
    unique_movies = list(
        {movie["id"]: movie for movie in movies}.values()
    )

    # Return 4 random recommendations
    return sample(unique_movies, k=min(4, len(unique_movies)))

def _my_picks_cache_key(data_path: Path) -> str:
    try:
        file_bytes = data_path.read_bytes()
    except OSError:
        return "my-picks:missing"

    digest = hashlib.sha256(file_bytes).hexdigest()
    return f"my-picks:{digest}"


def _load_my_picks_json(data_path: Path):
    try:
        with data_path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_my_picks():
    """Load curated picks from JSON and enrich them with TMDB details."""
    data_path = Path(__file__).resolve().parent / "data" / "my_picks.json"
    cache_key = _my_picks_cache_key(data_path)

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    curated_entries = _load_my_picks_json(data_path)
    if not curated_entries:
        cache.set(cache_key, [], timeout=300)
        return []

    prepared_picks = []
    for entry in curated_entries:
        tmdb_id = entry.get("tmdb_id")
        media_type = entry.get("media_type")

        if not tmdb_id or media_type not in {"movie", "tv"}:
            continue

        details_response = get_movie_tv_details(tmdb_id, media_type)
        if not details_response:
            continue

        details = get_necessary_details(details_response)
        if not details:
            continue

        details.update({
            "media_type": media_type,
            "note": entry.get("note", ""),
            "tags": entry.get("tags", []),
            "poster_url": f"https://image.tmdb.org/t/p/w342{details.get('poster')}" if details.get("poster") else None,
        })

        prepared_picks.append(details)

    cache.set(cache_key, prepared_picks, timeout=3600)
    return prepared_picks


def get_necessary_details(response):
    if not response:
        return None
    
    # TMDB's transparent title artwork. Prefer an English logo, then a
    # language-neutral one, so the detail page can use the official title art.
    logos = response.get("images", {}).get("logos", [])
    title_logo = next(
        (logo.get("file_path") for logo in logos if logo.get("iso_639_1") == "en"),
        None
    ) or next(
        (logo.get("file_path") for logo in logos if logo.get("iso_639_1") is None),
        None
    ) or next(
        (logo.get("file_path") for logo in logos),
        None
    )

    # Director
    director = None

    for person in response.get("credits", {}).get("crew", []):
        if person["job"] == "Director":
            director = person["name"]
            break

    
    # Top Cast (8)    
    cast = []   

    for actor in response.get("credits", {}).get("cast", [])[:10]:
        cast.append({
            "name": actor.get("name"),
            "original_name": actor.get("original_name") or actor.get("name"),
            "character": actor.get("character"),
            "profile": actor.get("profile_path")
        })

   
    # Trailer    
    trailer = None

    for video in response.get("videos", {}).get("results", []):

        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
        ):
            trailer = video["key"]
            break


   # Extract the country dictionary
    country_data = response.get("watch/providers", {}).get("results", {}).get("US", {})

    # Get each array (default to an empty list if missing)
    flatrate_list = country_data.get("flatrate", [])
    free_list     = country_data.get("free", [])
    ads_list      = country_data.get("ads", [])

    # Combine them all into one flat list
    watch_providers = flatrate_list + free_list + ads_list


    country_codes = (
    response.get("origin_country")
    or [
        country["iso_3166_1"]
        for country in response.get("production_countries", [])
    ]
)

    
    # Final Dictionary
    
    movie = {

        "adult": response.get("adult", False),

        "id": response.get("id"),

        "title": response.get("title") or response.get("name"),

        "title_logo": title_logo,

        "overview": response.get("overview", ""),

        "poster": response.get("poster_path"),

        "backdrop": response.get("backdrop_path"),

        "rating": response.get("vote_average", 0),

        "runtime": (
            response.get("runtime")
            or (
                response.get("episode_run_time", [None])[0]
                if response.get("episode_run_time")
                else None
            )
        ),

        "release_date": (
            response.get("release_date")
            or response.get("first_air_date")
        ),

        "genres": ", ".join(
            genre["name"]
            for genre in response.get("genres", [])
        ),

        "director": director,

        "cast": cast,

        "trailer": trailer,

        "watch_providers": watch_providers,

        "budget": usd(response.get("budget")),

        "revenue": usd(response.get("revenue")),

        "country": format_country(country_codes),

        "language": format_language(response.get("original_language")),

        "tagline": response.get("tagline"),

        "status": response.get("status"),

        "homepage": response.get("homepage"),

        "imdb_id": response.get("imdb_id")

    }

    return movie



def usd(value):
    """Format value as USD."""

    if not value:
        return "N/A"

    return f"${value:,.2f}"



def format_language(language_code):
    """Convert language code (en) -> English."""

    if not language_code:
        return None

    language = pycountry.languages.get(alpha_2=language_code)

    if language:
        return language.name

    return language_code


def format_country(country_codes):
    """Convert ['US', 'GB'] -> United States, United Kingdom."""

    if not country_codes:
        return None

    countries = []

    for code in country_codes:

        country = pycountry.countries.get(alpha_2=code)

        if country:
            countries.append(country.name)
        else:
            countries.append(code)

    return ", ".join(countries)


