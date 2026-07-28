from random import randint, sample
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
    params = {
        "sort_by": "popularity.desc",
        "include_adult": filters["adult"],
    }

    watch_type = filters.get("type")
    selected_year = filters.get("year")

    # Genre
    if filters.get("genre"):
        params["with_genres"] = filters["genre"]

    # Language
    if filters.get("language"):
        params["with_original_language"] = filters["language"]

    # Minimum Rating
    params["vote_average.gte"] = filters.get("rating") or 7

    # Movie-specific filters
    if watch_type == "movie":
        params["vote_count.gte"] = 2000

        if selected_year:
            params.update(MOVIE_ERA_MAPPING[selected_year])
        else:
            params["primary_release_date.gte"] = "1980-01-01"

    # TV-specific filters
    else:
        params["vote_count.gte"] = 500

        if selected_year:
            params.update(TV_ERA_MAPPING[selected_year])
        else:
            params["first_air_date.gte"] = "1980-01-01"

    return params


def discover_movies_tv(filters, watch_type="movie"):
    params = convert_filters_to_params(filters)

    response = discover_media(params, watch_type)

    total_pages = min(response.get("total_pages", 1), 500)

    start_page = randint(1, max(total_pages - 2, 1))

    movies = []

    for page in range(start_page, min(start_page + 3, total_pages + 1)):
        response = discover_media(params, watch_type, page)
        movies.extend(response.get("results", []))

    # Remove duplicates by TMDb ID
    unique_movies = {movie["id"]: movie for movie in movies}.values()

    unique_movies = list(unique_movies)

    return sample(unique_movies, k=min(4, len(unique_movies)))


def get_necessary_details(response):

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

    for person in response["credits"]["crew"]:
        if person["job"] == "Director":
            director = person["name"]
            break

    
    # Top Cast (8)    
    cast = []

    for actor in response["credits"]["cast"][:8]:

        cast.append({
            "name": actor.get("name"),
            "original_name": actor.get("original_name") or actor.get("name"),
            "character": actor.get("character"),
            "profile": actor.get("profile_path")
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


   # Extract the country dictionary
    country_data = response["watch/providers"]["results"].get("US", {})

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

        "adult": response["adult"],

        "id": response["id"],

        "title": response.get("title") or response.get("name"),

        "title_logo": title_logo,

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


def get_alt_providers(watch_type, tmdb_id):
    providers = [
        {
            "name": "Cineplay",
            "url": f"https://www.cineplay.to/{watch_type}/{tmdb_id}",
            "logo": "https://www.cineplay.to/logo.png"
        },
        
        {
            "name": "Skyflix",
            "url": f"https://www.skyflix.to/title/{watch_type}/{tmdb_id}",
            "logo": "https://www.skyflix.to/logo.png"
        },
        {
            "name": "Cineby",
            "url": f"https://cineby.tech/{watch_type}/{tmdb_id}/watch",
            "logo": "https://cineby.tech/cineby-logo@2x.webp"
        },
        {
            "name": "Dulo",
            "url": f"https://dulo.tv/",
            "logo": "https://dulo.tv/dulo-auth-mark.png"
        }
    ]


    if watch_type == "tv":
        providers.append({
            "name": "StreamFun",
            "url": f"https://streamfun.space/watch/{watch_type}/{tmdb_id}?s=1&ep=1",
            "logo": "https://streamfun.space/streamfun_icon.png"
        })
    else:
        providers.append({
            "name": "StreamFun",
            "url": f"https://streamfun.space/watch/movie/{tmdb_id}",
            "logo": "https://streamfun.space/streamfun_icon.png"
        })

    return providers

