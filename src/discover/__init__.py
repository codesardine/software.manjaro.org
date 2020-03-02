from flask import Flask
from flask_caching import Cache
from discover.templateUtils import truncate_description
app = Flask(__name__)
cache = Cache(app, config={
    "CACHE_TYPE": "filesystem",
    'CACHE_DIR': './data/cache',
    "CACHE_DEFAULT_TIMEOUT": 3600
})
app.jinja_env.filters['truncate_description'] = truncate_description
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


import discover.views
