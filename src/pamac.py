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

    def individual_repo_pkgs(self, repo):
        return self.database.get_repo_pkgs(repo)

    def all_repo_pkgs(self, pkgs_name):
        if pkgs_name == pkgs_name and isinstance(pkgs_name, str):
            pkgs = []
            for repository in self.database.get_repos_names():
                for package in self.database.get_repo_pkgs(repository):
                    icon = package.get_icon()
                    if not icon and pkgs_name == "Packages":
                        pkgs.append(package)
                    elif icon and pkgs_name == "Applications":
                        pkgs.append(package)
                    else:
                        name = pkgs_name.lower()
                        if name in package.get_packager() and name in package.get_url(): # TODO FIX: only apps ?
                            pkgs.append(package)
            pkgs.sort(key=methodcaller("get_name"))
            return pkgs
        else:
            return self.database.get_category_pkgs(name)
