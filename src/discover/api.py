"""
export databases to json

"""
import sys
from datetime import datetime
from operator import methodcaller
from flask import jsonify
import discover.render as render

class Worker:
    """ all databases to same json """
    def __init__(self, idx: int):
        self.datas = []
        self.title = ""
        if idx > -1:
            self.title = render.get_categories()[idx].get("title")

    def _getHeader(self):
        return {
            "status": 200,
            "items": [],
            "title": self.title,
            "count": 0,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    def _includeItem(self, item, detail=False):
        pass

    def get_all(self):
        #self.datas.sort(key=methodcaller("get_name"))
        self.datas = tuple(self.datas)
        sorted(self.datas, key=methodcaller("get_name"))

    def get_package(self, package_name):
        self.datas = ()
        pkg = render.get.database.get_sync_pkg(package_name)
        if pkg:
            self.datas = (pkg,)

    def to_json(self, option: str = ""):
        ret = self._getHeader()
        detail = len(self.datas) == 1
        ret["count"] = len(self.datas)
        try:
            if option != "count":
                # return only one field
                if option == "name":
                    for item in self.datas:
                        ret["items"].append(item.get_name())
                elif option == "app":
                    for item in self.datas:
                        ret["items"].append(item.get_app_name())
                # filters packages
                elif option.startswith("url@"):
                    option = option[4:].lower()
                    self.datas = tuple(x for x in self.datas if option in x.get_url().lower())
                    for item in self.datas:
                        ret["items"].append(self._includeItem(item, detail))
                    ret["count"] = len(self.datas)
                elif option.startswith("desc@"):
                    option = option[5:].lower()
                    self.datas = tuple(x for x in self.datas if option in x.get_desc().lower())
                    for item in self.datas:
                        ret["items"].append(self._includeItem(item, detail))
                    ret["count"] = len(self.datas)
                elif option.startswith("dep@"):
                    option = option[4:].lower()
                    self.datas = tuple(x for x in self.datas if option in x.get_depends())
                    for item in self.datas:
                        ret["items"].append(self._includeItem(item, detail))
                    ret["count"] = len(self.datas)
                # default return all
                else:
                    for item in self.datas:
                        ret["items"].append(self._includeItem(item, detail))

            if ret["count"] < 1:
                ret["status"] = 404
        except:
            ret["status"] = 500
            print(f"Api Error: {sys.exc_info()[0]}")
        return jsonify(ret)

    @staticmethod
    def is_manjaro(pkg) ->int:
        if "manjaro.org" in pkg.get_url():
            return 1
        if "manjaro.org" in pkg.get_packager():
            return 2
        return 0

    @staticmethod
    def is_gtk(pkg) ->bool:
        if "gtk3" in set(pkg.get_depends()):
            return True
        if "gnome.org" in pkg.get_url():
            return True
        return False

    @staticmethod
    def is_qt(pkg) ->bool:
        if "qt5-base" in set(pkg.get_depends()):
            return True
        return False

    @staticmethod
    def is_plasma(pkg) ->bool:
        if "kde-applications" in set(pkg.get_groups()):
            return True
        deps = set(pkg.get_depends())
        if "plasma-workspace" in deps or "plasma-framework" in deps:
            return True
        return False


class ApplicationsWorker(Worker):

    def get_all(self):
        self.datas = render.get.all_repo_pkgs(self.title)
        super().get_all()

    def _includeItem(self, item, detail=False):
        icon = item.get_icon().replace('/usr/share/app-info/', '')
        if detail:
            ret = {}
            for prop in item.props:
                key = prop.name
                value = item.get_property(prop.name)
                if key == "icon":
                    value = icon
                if value:
                    ret[prop.name] = value
            manja = self.is_manjaro(item)
            if manja > 0:
                ret['manjaro'] = manja
            if self.is_gtk(item):
                ret['gtk'] = 1
            if self.is_plasma(item):
                ret['plasma'] = 1
            if self.is_qt(item):
                ret['qt'] = 1
            return ret
        ret = {
            'pkg': item.get_name(),
            'name': item.get_app_name(),
            'url': item.get_url(),
            'icon': icon,
            'desc': item.get_desc(),
        }
        if self.is_gtk(item):
            ret['gtk'] = 1
        if self.is_plasma(item):
            ret['plasma'] = 1
        if self.is_qt(item):
            ret['qt'] = 1
        return ret


class PackagesWorker(Worker):
    def get_all(self):
        self.datas = render.get.all_repo_pkgs(self.title)
        super().get_all()

    def _includeItem(self, item, detail=False):
        if detail:
            ret = {}
            for prop in item.props:
                key = prop.name
                value = item.get_property(prop.name)
                if key == "icon":
                    value = "images/package.svg"
                    if self.is_manjaro(item) == 1:
                        value = "images/favicon.png"
                if value:
                    ret[prop.name] = value
            manja = self.is_manjaro(item)
            if manja > 0:
                ret['manjaro'] = manja
            if self.is_gtk(item):
                ret['gtk'] = 1
            if self.is_plasma(item):
                ret['plasma'] = 1
            if self.is_qt(item):
                ret['qt'] = 1
            return ret
        ret = {
            'name': item.get_name(),
            'url': item.get_url(),
            #'icon': "images/package.svg",
            'desc': item.get_desc(),
        }
        if self.is_gtk(item):
            ret['gtk'] = 1
        if self.is_plasma(item):
            ret['plasma'] = 1
        if self.is_qt(item):
            ret['qt'] = 1
        #if self.is_manjaro(item) == 1:
        #    ret['icon'] = "images/favicon.png"
        return ret


class SnapWorker(Worker):
    def get_all(self):
        database = render.get.external_repos()[1]
        for category in render.get.external_repos()[0]:
            cat = database.get_category_snaps(category)
            for app in cat:
                self.datas.append(app)
        super().get_all()

    def _includeItem(self, item, detail=False):
        if detail:
            ret = {}
            for prop in item.props:
                value = item.get_property(prop.name)
                if value:
                    ret[prop.name] = value
            return ret
        return {
            'name': item.get_name(),
            'url': item.get_url(),
            'icon': item.get_icon(),
            'desc': item.get_desc(),
        }

    def get_package(self, package_name):
        self.datas = ()
        database = render.get.external_repos()[1]
        for category in render.get.external_repos()[0]:
            cat = database.get_category_snaps(category)
            for app in cat:
                if app.get_name() == package_name:
                    self.datas = (app,)
                    return

'''
class CategoriesWorker(Worker):
    def getAll(self):
        self.datas = render.get_categories()

    def _includeItem(self, item):
        return item
'''
