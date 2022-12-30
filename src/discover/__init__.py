from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/discover.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

scheduler = APScheduler()
scheduler.api_enabled = False

from discover import views
from discover import Utils
from discover.templates import filters

app.jinja_env.filters['truncate_description'] = filters.truncate_description
app.jinja_env.filters['remove_pkg_symbols'] = filters.remove_pkg_symbols
app.jinja_env.filters['split_version'] = filters.split_version

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
Utils.update_system()

@scheduler.task('interval', id='update', minutes=1440, max_instances=1)
def update():
   Utils.update_system()
    
scheduler.init_app(app)
scheduler.start()




