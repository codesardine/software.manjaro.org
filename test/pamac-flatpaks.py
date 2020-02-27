#!/usr/bin/python3

from gi.repository import Pamac
import gi
gi.require_version('Pamac', '9.0')

config = Pamac.Config(conf_path="/etc/pamac.conf")
db = Pamac.Database(config=config)

db.enable_appstream()
name = db.get_categories_names()
for cat in name:
    cat = db.get_category_flatpaks(cat)
    for i in cat:
        print(i.get_app_name())
