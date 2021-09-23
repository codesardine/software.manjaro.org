from flask import Flask
from flask_caching import Cache
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cache = Cache(app, config={
    "CACHE_TYPE": "filesystem",
    'CACHE_DIR': './data/cache',
    "CACHE_DEFAULT_TIMEOUT": 3600
})

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///discover.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

sql = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.api_enabled = False

from discover import views, Utils

app.jinja_env.filters['truncate_description'] = Utils.truncate_description
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@scheduler.task('interval', id='update', minutes=1440, max_instances=1)
def update():
    Utils.update_system()
    
update()
scheduler.init_app(app)
scheduler.start()
