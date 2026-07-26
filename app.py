from flask import Flask, redirect, render_template, request
from random import sample

# My methods
from tmdb_service import get_movie_genres, get_all_languages, discover_movies_tv
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

    # Convert the filters to parameters for the API request
    params = convert_filters_to_params(filters)   

    # Get the results from TMDB
    if watch_type:
        result = discover_movies_tv(params, watch_type)
    else:
        return render_template('error.html',
                               msg="Invalid Watch Type")  

    # If returned result does not have 4 or more Movies/TV-Shows
    # Show error
    if len(result) < 4:
        return render_template('error.html',
                               msg="Movies/TV-Shows with such filters does not exist. Try changing the filters") 
    # Randomly sample only 4
    random_samples = sample(result, k=4)    

    return render_template('components/recommendations.html',
                           random_samples=random_samples,
                           watch_type=watch_type)
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"