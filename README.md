# WhatToWatch

WhatToWatch is a Flask web app that helps you discover movies and TV shows based on your mood or custom filters using TMDB data.

## Features

- Browse trending movies and TV shows
- Search for movies and TV shows
- Discover recommendations using mood or custom filters
- View detailed information, including cast, trailers, ratings, and streaming providers
- Explore a curated **My Picks** collection with personal recommendations

## Setup

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your TMDB API key as an environment variable or in a `.env` file:

   ```text
   TMDB_API_KEY=your_api_key_here
   ```

3. Start the development server:

   ```bash
   flask run
   ```

## Project Structure

```
app.py                         # Application entry point
what_to_watch/
├── routes.py                  # Flask routes
├── helpers.py                 # Helper functions
├── services/
│   └── tmdb.py                # TMDB API integration
├── templates/                 # Jinja templates
├── static/                    # CSS, JavaScript, images
└── data/
    └── my_picks.json          # Curated recommendations
```

## Credits

Movie and TV data is provided by TMDB.