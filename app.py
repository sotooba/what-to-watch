from flask import Flask, redirect, render_template, request

# My methods
from tmdb_service import get_movie_genres, get_tv_genres, get_all_languages
from helpers import get_popular_languages, discover_movies_tv
from const_data import MOODS, YEAR_OPTIONS, RATING_OPTIONS, MOOD_FILTERS

app = Flask(__name__)



# Return aplogy (error) if something goes wrong
def apology(message):
    return render_template('error.html', msg=message)



# Shows the home page
@app.route('/')
def index():
    msg = "Could not load Genres & Language data. Try connecting with internet or use Mood."

    movie_genres = get_movie_genres()
    if not movie_genres:
        return apology(msg)
    
    tv_genres = get_tv_genres()
    if not tv_genres:
        return apology(msg)

    languages = get_popular_languages(get_all_languages())
    if not languages:
            return apology(msg)
    
    return render_template('index.html', 
                            movie_genres=movie_genres, 
                            tv_genres=tv_genres, 
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

    result = discover_movies_tv(filters, watch_type)


    if len(result) == 0:
        return apology("We couldn't find anything for you. Change the filters and Try Again.")
    
    

    return render_template('components/recommendations.html',
                           random_samples=result,
                           watch_type=watch_type)

    

@app.route('/recommendation/mood/<mood>')
def mood_recommendation(mood):
    filters = MOOD_FILTERS.get(mood)
    filters["adult"] = request.form.get("adult") == "true"

    result = discover_movies_tv(filters)
    if len(result) == 0:
            return apology("We couldn't find anything for you. Change the filters and Try Again.")

    return render_template('components/recommendations.html',
                            random_samples=result,
                            watch_type="movie")



@app.route('/recommendation/<string:watch_type>/<int:tmdb_id>')
def recommendation_click(watch_type, tmdb_id):
    # Ensure you are using an f-string so {movie_id} renders as a number
    return f"it worked and type is {watch_type} and id is {tmdb_id}"




@app.route('/about')
def about():
    return "about"

@app.route('/search')
def search():
    return "search page"

@app.route('/trending')
def trending():
    return "trending media type"