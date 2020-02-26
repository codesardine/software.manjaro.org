#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)
from routes import *

if __name__ == "__main__":
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.run(port=8000, host="127.0.0.1", debug=True)
