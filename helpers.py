def get_popular_languages(all_languages):
    """
    Takes a list of all languages.

    Returns:
        set: A set of popular languages (sorted alphabetically).
    """
    popular_languages = {
        "en",  # English
        "hi",  # Hindi
        "ja",  # Japanese
        "ko",  # Korean
        "fr",  # French
        "es",  # Spanish
        "de",  # German
        "it",  # Italian
        "zh",  # Chinese
        "ru",  # Russian
        "ar",  # Arabic
        "tr",  # Turkish
        "th",  # Thai
        "te",  # Telugu
        "ml",  # Malayalam
    }

    filtered_languages = []

    for language in all_languages:
        if language["iso_639_1"] in popular_languages:
            filtered_languages.append(language)
    
    return sorted(filtered_languages, key=lambda d: d["english_name"])
