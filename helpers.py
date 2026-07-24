from const_data import POPULAR_LANGUAGES 

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
