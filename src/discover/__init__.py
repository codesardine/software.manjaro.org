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
app.config['IS_MAINTENANCE_MODE'] = True


sql = SQLAlchemy(app, session_options={"autoflush": False})
scheduler = APScheduler()
scheduler.api_enabled = False

from discover import views, Utils
from discover.templates import filters

app.jinja_env.filters['truncate_description'] = filters.truncate_description
app.jinja_env.filters['remove_pkg_symbols'] = filters.remove_pkg_symbols
app.jinja_env.filters['split_version'] = filters.split_version

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@scheduler.task("date", id="update_on_deploy", run_date=None)
def update_on_deploy():
    database.Database().reload_tables()
    app.config['IS_MAINTENANCE_MODE'] = False

@scheduler.task('interval', id='update', minutes=1440, max_instances=1)
def update():
    Utils.update_system()
    
scheduler.init_app(app)
scheduler.start()
