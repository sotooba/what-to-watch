import os

from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from .extensions import cache


def create_app(test_config=None):
    """Create and configure the WhatToWatch Flask application."""
    load_dotenv()

    app = Flask(__name__)
    
    app.config.from_mapping(
        TMDB_API_KEY=os.getenv("TMDB_API_KEY"),
        CACHE_TYPE="SimpleCache",
        CACHE_DEFAULT_TIMEOUT=300,
        CACHE_THRESHOLD=1_000,
        TMDB_CACHE_TTLS={
            "configuration": 60 * 60 * 24 * 30,
            "details": 60 * 60 * 6,
            "discover": 60 * 15,
            "popular": 60 * 60 * 24,
            "search": 60 * 15,
            "trending": 60 * 60 * 24,
        },
    )

    if test_config:
        app.config.update(test_config)

    cache.init_app(app)

    from .routes import web

    app.register_blueprint(web)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template(
            "error.html",
            msg="We couldn't find that page. It may have moved or the link may be incomplete.",
        ), 404

    @app.errorhandler(HTTPException)
    def http_error(error):
        return render_template(
            "error.html",
            msg="That request isn't available right now. Please try again.",
        ), error.code

    @app.errorhandler(Exception)
    def unexpected_error(error):
        app.logger.exception("Unexpected application error: %s", error)
        return render_template(
            "error.html",
            msg="Something unexpected interrupted that request. Please try again.",
        ), 500

    return app
