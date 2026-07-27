from random import sample
import pycountry

# My methods
from const_data import POPULAR_LANGUAGES, MOVIE_ERA_MAPPING, TV_ERA_MAPPING
from tmdb_service import  discover_media


def get_popular_languages(all_languages):
    filtered_languages = []

    for language in all_languages:
        if language["iso_639_1"] in POPULAR_LANGUAGES:
            filtered_languages.append(language)
    
    return sorted(filtered_languages, key=lambda d: d["english_name"])


def convert_filters_to_params(filters):
    params = {}

    # Genre
    if filters.get("genre"):
        params["with_genres"] = filters["genre"]

    # Year as per watch_type
    if filters.get("type") == "movie":    
        era = filters.get("year")
        if era in MOVIE_ERA_MAPPING:
            params.update(MOVIE_ERA_MAPPING[era])
    else:
        era = filters.get("year")
        if era in TV_ERA_MAPPING:
            params.update(TV_ERA_MAPPING[era])

    # Language
    if filters.get("language"):
        params["with_original_language"] = filters["language"]

    # Rating
    if filters.get("rating"):
        params["vote_average.gte"] = filters["rating"]

    # Adult Content
    params["include_adult"] = filters["adult"]
    
    return params


def discover_movies_tv(filters, watch_type="movie"):
    params = convert_filters_to_params(filters)
    result = discover_media(params, watch_type) 

    # Randomly sample only 4
    return sample(result, k=min(4, len(result)))


def get_necessary_details(response):

    # Director
    director = None

    for person in response["credits"]["crew"]:
        if person["job"] == "Director":
            director = person["name"]
            break

    
    # Top Cast (8)    
    cast = []

    for actor in response["credits"]["cast"][:8]:

        cast.append({
            "name": actor["name"],
            "character": actor["character"],
            "profile": actor["profile_path"]
        })

   
    # Trailer    
    trailer = None

    for video in response["videos"]["results"]:

        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
        ):
            trailer = video["key"]
            break


    # Watch Providers (Pakistan)    
    watch_providers = (
        response["watch/providers"]["results"]
        .get("US", {})
        .get("flatrate", [])
    )

    country_codes = (
    response.get("origin_country")
    or [
        country["iso_3166_1"]
        for country in response.get("production_countries", [])
    ]
)

    
    # Final Dictionary
    
    movie = {

        "adult": response["adult"],

        "id": response["id"],

        "title": response.get("title") or response.get("name"),

        "overview": response["overview"],

        "poster": response["poster_path"],

        "backdrop": response["backdrop_path"],

        "rating": response["vote_average"],

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
            for genre in response["genres"]
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