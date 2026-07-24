from flask import Flask, render_template, request
from tmdb_service import get_movie_genres, get_all_languages
from helpers import get_popular_languages

app = Flask(__name__)

@app.route('/')
def index():
    genres = get_movie_genres()
    languages = get_popular_languages(get_all_languages())
    return render_template('index.html', genres=genres, languages=languages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"