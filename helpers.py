from flask import render_template
from random import sample

# My methods
from const_data import POPULAR_LANGUAGES, MOVIE_ERA_MAPPING, TV_ERA_MAPPING
from tmdb_service import  discover_media


# Return aplogy (error) if something goes wrong
def apology(message):
    return render_template('error.html', msg=message)


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


def discover_movies_tv(filters):
    params = convert_filters_to_params(filters) 
    result = discover_media(params) 
    
    if len(result) < 4:
        return apology("We couldn't find anything for you. Change the filters and Try Again.")

    # Randomly sample only 4
    return sample(result, k=4)
    