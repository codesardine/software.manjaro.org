import gi
gi.require_version('Pamac', '9.0')
from gi.repository import Pamac


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
