#!/usr/bin/python3

from gi.repository import Pamac
import gi
gi.require_version('Pamac', '9.0')
import gi

config = Pamac.Config(conf_path="/etc/pamac.conf")
db = Pamac.Database(config=config)
name = "gimp"
repo =db.search_repos_pkgs(name)
for pkg in repo:
  if pkg.get_name() == name:
    print(pkg.get_name())
