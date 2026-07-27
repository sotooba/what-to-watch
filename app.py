from flask import Flask, redirect, render_template, request

# My methods
from tmdb_service import get_movie_genres, get_all_languages
from helpers import get_popular_languages, discover_movies_tv, apology
from const_data import MOODS, YEAR_OPTIONS, RATING_OPTIONS, MOOD_FILTERS

app = Flask(__name__)



# Shows the home page
@app.route('/')
def index():
    msg = "Could not load necessary data. Try connecting with internet or try later"

    genres = get_movie_genres()
    if not genres:
        return apology(msg)

    languages = get_popular_languages(get_all_languages())
    if not languages:
            return apology(msg)
    
    return render_template('index.html', 
                            genres=genres, 
                            languages=languages,
                            moods=MOODS,
                            years=YEAR_OPTIONS,
                            ratings=RATING_OPTIONS)



# Calls the API and fetches Movie / TV-Show
@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Get the filters from the form submission
    filters = request.form.to_dict()

    # If adult is not selected, it will return None
    # Explicitly set it to false if not selected
    filters["adult"] = request.form.get("adult") == "true"

    # Get the watch type
    watch_type = filters["type"]

    result = discover_movies_tv(filters)

    return render_template('components/recommendations.html',
                           random_samples=result)

    

@app.route('/recommendation/mood/<mood>')
def recommendation(mood):
    filters = MOOD_FILTERS.get(mood)
    filters["adult"] = request.form.get("adult") == "true"

    result = discover_movies_tv(filters)

    return render_template('components/recommendations.html',
                               random_samples=result)






@app.route('/about')
def about():
    return "about"

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"