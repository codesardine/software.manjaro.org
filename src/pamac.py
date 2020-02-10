import gi
gi.require_version('Pamac', '9.0')
from gi.repository import Pamac
from operator import methodcaller

class Get:

    def __init__(self):
        self.config = Pamac.Config(conf_path="/etc/pamac.conf")
        database = Pamac.Database(config=self.config)
        database.enable_appstream()
        self.database = database

    def appstream_category(self, category):
        return self.database.get_category_pkgs(category)

    def repo(self, repo):
        return self.database.get_repo_pkgs(repo)

    def manjaro_category(self, category):
        if category == "Manjaro":
            pkgs = []
            for r in self.database.get_repos_names():
                print(r)
                for p in self.database.get_repo_pkgs(r):
                    if "manjaro" in p.get_packager() and "manjaro" in p.get_url(): # TODO FIX: only apps ?
                        pkgs.append(p)
            pkgs.sort(key=methodcaller("get_name"))
            return pkgs
        else:
            return self.database.get_category_pkgs(category)
