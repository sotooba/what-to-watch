from flask import Flask, render_template, request
from tmdb_service import get_movie_genres, get_all_languages
from helpers import get_popular_languages
from const_data import MOODS, YEAR_OPTIONS, RATING_OPTIONS

app = Flask(__name__)

@app.route('/')
def index():
    genres = get_movie_genres()
    languages = get_popular_languages(get_all_languages())
    moods = MOODS
    years = YEAR_OPTIONS
    ratings = RATING_OPTIONS

    return render_template('index.html', 
                            genres=genres, 
                            languages=languages,
                            moods=moods,
                            years=years,
                            ratings=ratings)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"