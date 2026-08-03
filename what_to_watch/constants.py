# Selected popular languages
POPULAR_LANGUAGES = {
        "en",  # English
        "hi",  # Hindi
        "ur",  # Urdu
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


# Mood Pods for premade filters
MOODS = [
    {
        "emoji": "✨",
        "title": "Happy",
        "subtitle": "Joy in every scene",
        "value": "happy"
    },
    {
        "emoji": "🌧️",
        "title": "Emotional",
        "subtitle": "Stories that stay",
        "value": "emotional"
    },
    {
        "emoji": "🍕",
        "title": "Family Night",
        "subtitle": "Fun For Everyone",
        "value": "family"
    },
    {
        "emoji": "💘",
        "title": "Love & Laughter",
        "subtitle": "Feel Every Moment",
        "value": "love"
    },
    {
        "emoji": "💀",
        "title": "Horror Night",   
        "subtitle": "Enter if you dare",
        "value": "horror"
    },
    {
        "emoji": "🤷‍♂️",
        "title": "Not Sure",
        "subtitle": "Find your next favorite",
        "value": "not_sure"
    }
]


# Year options for filtering
YEAR_OPTIONS = [
    {
        "label": "2020s",
        "value": "2020s"
    },
    {
        "label": "2010s",
        "value": "2010s"
    },
    {
        "label": "2000s",
        "value": "2000s"
    },
    {
        "label": "1990s",
        "value": "1990s"
    },
    {
        "label": "Classic",
        "value": "Classic"
    },
]


# Rating options for filtering
RATING_OPTIONS = [
    {
        "label": "⭐ 8.0+",
        "value": "8"
    },
    {
        "label": "⭐ 7.0+",
        "value": "7"
    },
    {
        "label": "⭐ 6.0+",
        "value": "6"
    },
]


# Converting year options to TMDB API parameters
MOVIE_ERA_MAPPING = {
    "classic": {
        "primary_release_date.lte": "1989-12-31"
    },
    "1990s": {
        "primary_release_date.gte": "1990-01-01",
        "primary_release_date.lte": "1999-12-31"
    },
    "2000s": {
        "primary_release_date.gte": "2000-01-01",
        "primary_release_date.lte": "2009-12-31"
    },
    "2010s": {
        "primary_release_date.gte": "2010-01-01",
        "primary_release_date.lte": "2019-12-31"
    },
    "2020s": {
        "primary_release_date.gte": "2020-01-01",
        "primary_release_date.lte": "2029-12-31"
    }
}

TV_ERA_MAPPING = {
    "classic": {
            "first_air_date.lte": "1989-12-31"
        },
        "1990s": {
            "first_air_date.gte": "1990-01-01",
            "first_air_date.lte": "1999-12-31"
        },
        "2000s": {
            "first_air_date.gte": "2000-01-01",
            "first_air_date.lte": "2009-12-31"
        },
        "2010s": {
            "first_air_date.gte": "2010-01-01",
            "first_air_date.lte": "2019-12-31"
        },
        "2020s": {
            "first_air_date.gte": "2020-01-01",
            "first_air_date.lte": "2029-12-31"
        }
}


MOOD_FILTERS = {
    "happy": {
        "genre": "35|10751|16",      # Comedy, Family, Animation
        "rating": "7",
    },

    "emotional": {
        "genre": "18|10749",         # Drama, Romance
        "rating": "7",
    },

    "family": {
        "genre": "10751|16",         # Family, Animation
        "rating": "7",
    },

    "love": {
        "genre": "10749|35",         # Romance, Comedy
        "rating": "7",
    },

    "horror": {
        "genre": "27",               # Horror only
        "rating": "7",
    },

    "not_sure": {
        "genre": "28|12|878|80",        # Action, Adventure, Sci-Fi
        "rating": "7",
    },
}

