from flask import Blueprint, render_template, request

from .constants import MOODS, MOOD_FILTERS, RATING_OPTIONS, YEAR_OPTIONS
from .helpers import discover_movies_tv, get_alt_providers, get_necessary_details, get_popular_languages
from .services.tmdb import (
    get_all_languages,
    get_movie_genres,
    get_movie_tv_details,
    get_popular,
    get_search_results,
    get_trending,
    get_tv_genres,
)


web = Blueprint("web", __name__)
CONNECTION_ERROR = "We couldn't reach TMDB right now. Check your connection and try again in a moment."


def apology(message, status=200):
    return render_template("error.html", msg=message), status


@web.route("/")
def index():
    movie_genres = get_movie_genres()
    tv_genres = get_tv_genres()
    languages = get_popular_languages(get_all_languages())

    if not movie_genres or not tv_genres or not languages:
        return apology("Could not load genres and languages. Check your connection and try again.")

    return render_template(
        "index.html",
        movie_genres=movie_genres,
        tv_genres=tv_genres,
        languages=languages,
        moods=MOODS,
        years=YEAR_OPTIONS,
        ratings=RATING_OPTIONS,
    )


@web.route("/recommendations", methods=["POST"])
def recommendations():
    filters = request.form.to_dict()
    filters["adult"] = request.form.get("adult") == "true"
    watch_type = filters.get("type", "movie")

    if watch_type not in {"movie", "tv"}:
        return apology("Choose movies or TV shows, then try again.")

    results = discover_movies_tv(filters, watch_type)
    if results is None:
        return apology(CONNECTION_ERROR)
    if not results:
        return apology("We couldn't find anything for you. Change the filters and try again.")

    return render_template("components/recommendations.html",
                           random_samples=results,
                           watch_type=watch_type)


@web.route("/recommendations/mood/<mood>")
def mood_recommendations(mood):
    mood_filters = MOOD_FILTERS.get(mood)
    if not mood_filters:
        return apology("That mood isn't available. Choose another vibe and try again.")

    results = discover_movies_tv({**mood_filters, "type": "movie", "adult": False})
    if results is None:
        return apology(CONNECTION_ERROR)
    if not results:
        return apology("We couldn't find anything for that mood. Try another vibe.")

    return render_template("components/recommendations.html",
                           random_samples=results,
                           watch_type="movie")


@web.route("/<watch_type>/<int:tmdb_id>")
def recommendation_click(watch_type, tmdb_id):
    if watch_type not in {"movie", "tv"}:
        return apology("We couldn't open that title. Please choose a movie or TV show and try again.")

    movie = get_necessary_details(get_movie_tv_details(tmdb_id, watch_type))
    if not movie:
        return apology(CONNECTION_ERROR)

    return render_template(
        "components/modal.html",
        movie=movie,
        providers=get_alt_providers(watch_type, tmdb_id),
    )


def _render_media_collection(title, movies, shows):
    if not movies and not shows:
        return apology(CONNECTION_ERROR)
    return render_template("trending.html",
                           title=title,
                           movies=movies,
                           tv_shows=shows)


@web.route("/trending/today")
def trending_today():
    return _render_media_collection("Trending Today",
                                    get_trending("movie", "day"),
                                    get_trending("tv", "day"))


@web.route("/trending/weekly")
def trending_weekly():
    return _render_media_collection("Trending Weekly",
                                    get_trending("movie", "week"),
                                    get_trending("tv", "week"))


@web.route("/popular")
def get_popular_media():
    return _render_media_collection("Popular",
                                    get_popular("movie"),
                                    get_popular("tv"))


@web.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return apology("Search for something to view the results.")

    media_items = [
        item for item in get_search_results(query)
        if item.get("media_type") in {"movie", "tv"}
    ]
    if not media_items:
        return apology(f"We couldn't find movies or shows for '{query}'. Check the spelling or try something else.")

    return render_template("search.html",
                           query=query,
                           media_items=media_items)


@web.route("/about")
def about():
    return render_template("about.html")
