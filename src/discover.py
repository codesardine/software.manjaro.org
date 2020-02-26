#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)
from routes import *
from templateutils import *


if __name__ == "__main__":
    app.jinja_env.filters['trunc_desc'] = truncate_desc
    app.jinja_env.filters['class_manjaro'] = get_class_manjaro
    app.run(port=8000, host="127.0.0.1", debug=True)
