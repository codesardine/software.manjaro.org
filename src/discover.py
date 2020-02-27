#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)
from routes import *
from templateUtils import *


if __name__ == "__main__":
    # this only works on debugind not with wsgi server
    app.jinja_env.filters['truncate_description'] = truncate_description
    app.run(port=8000, host="127.0.0.1", debug=True)
