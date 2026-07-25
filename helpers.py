from const_data import POPULAR_LANGUAGES, ERA_MAPPING

def get_popular_languages(all_languages):
    """
    Takes a list of all languages.

    Returns:
        A list of popular languages (sorted alphabetically).
    """
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

    # Year
    era = filters.get("year")
    if era in ERA_MAPPING:
        params.update(ERA_MAPPING[era])

    # Language
    if filters.get("language"):
        params["with_original_language"] = filters["language"]

    # Rating
    if filters.get("rating"):
        params["vote_average.gte"] = filters["rating"]

    # Adult Content
    params["include_adult"] = filters["adult"]
    
    return params
