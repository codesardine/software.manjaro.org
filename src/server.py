from flask import Flask
app = Flask(__name__)
from routes import *

app.run(port=8080, host="127.0.0.1")
