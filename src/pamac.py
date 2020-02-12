from functools import lru_cache as cache
from operator import methodcaller
import gi
gi.require_version('Pamac', '9.0')
from gi.repository import Pamac


class Get:

    def __init__(self):
        self.config = Pamac.Config(conf_path="/etc/pamac.conf")
        database = Pamac.Database(config=self.config)
        database.enable_appstream()
        self.database = database

    @cache(maxsize=128)
    def appstream_category(self, category):
        return self.database.get_category_pkgs(category)

    @cache(maxsize=128)
    def individual_repo_pkgs(self, repo):
        return self.database.get_repo_pkgs(repo)

    @cache(maxsize=128)
    def all_repo_pkgs(self, title):
        if title == title and isinstance(title, str):
            pkgs = []
            for repository in self.database.get_repos_names():
                for package in self.database.get_repo_pkgs(repository):
                    icon = package.get_icon()
                    if not icon and title == "Packages":
                        pkgs.append(package)
                    elif icon and title == "Applications":
                        pkgs.append(package)
                    else:
                        name = title.lower()
                        if name in package.get_packager() and name in package.get_url():  # TODO FIX: only apps ?
                            pkgs.append(package)
            pkgs.sort(key=methodcaller("get_name"))
            return pkgs
        else:
            return self.database.get_category_pkgs(name)

    @cache(maxsize=128)
    def all_snaps(self):
        # FIXME some unknown categories are missing
        snap_categories = self.database.get_categories_names ()
        return snap_categories, self.database
