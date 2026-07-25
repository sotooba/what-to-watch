from flask import Flask, redirect, render_template, request
from random import sample

# My methods
from tmdb_service import get_movie_genres, get_all_languages, discover_movies
from helpers import get_popular_languages, convert_filters_to_params
from const_data import MOODS, YEAR_OPTIONS, RATING_OPTIONS

app = Flask(__name__)

# Shows the home page
@app.route('/')
def index():
    # Returns the index.html template with the necessary data for rendering the page.
    return render_template('index.html', 
                            genres=get_movie_genres(), 
                            languages=get_popular_languages(get_all_languages()),
                            moods=MOODS,
                            years=YEAR_OPTIONS,
                            ratings=RATING_OPTIONS)



@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Get the filters from the form submission
    filters = request.form.to_dict()
    filters["adult"] = request.form.get("adult") == "true"

    # Convert the filters to parameters for the API request
    params = convert_filters_to_params(filters)
    movies = discover_movies(params)

    # Randomly sample only 4
    random_movies = sample(movies, k=4)

    return render_template('components/recommendations.html',
                           movies=random_movies)
    


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"