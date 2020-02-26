#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)
from views import *

if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1", debug=True)
