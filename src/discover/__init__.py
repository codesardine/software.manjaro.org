from flask import Flask
from discover.templateUtils import truncate_description
app = Flask(__name__)
app.jinja_env.filters['truncate_description'] = truncate_description

import discover.views
