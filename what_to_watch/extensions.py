from flask_caching import Cache


# The extension is initialised by the application factory, avoiding circular imports.
cache = Cache()
