"""
export databases to json

"""
import sys
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
        }

    def _includeItem(self, item, detail=False):
        pass

    def getAll(self):
        pass

    def getPackage(self, package_name):
        self.datas = []
        pkg = render.get.database.get_sync_pkg(package_name)
        if pkg:
            self.datas.append(pkg)

    def toJson(self, detail=False):
        detail = len(self.datas) == 1
        ret = self._getHeader()
        try:
            #i = 0
            for item in self.datas:
                #i = i +1
                #if i > 400: # for test linit size
                #    break
                ret["items"].append(self._includeItem(item, detail))
            ret["count"] = len(ret["items"])
            if ret["count"] < 1:
                ret["status"] = 404
        except:
            ret["status"] = 500
            print(f"Api Error: {sys.exc_info()[0]}")
        return jsonify(ret)

    @staticmethod
    def is_manjaro(pkg) ->int:
        if "manjaro.org" in pkg.props.url:
            return 1
        if "manjaro.org" in pkg.props.packager:
            return 2
        return 0

    @staticmethod
    def is_gtk(pkg) ->bool:
        if "gtk3" in set(pkg.props.depends):
            return True
        if "gnome.org" in pkg.props.url:
            return True
        return False

    @staticmethod
    def is_qt(pkg) ->bool:
        if "qt5-base" in set(pkg.props.depends):
            return True
        return False

    @staticmethod
    def is_plasma(pkg) ->bool:
        if "kde-applications" in set(pkg.props.groups):
            return True
        deps = set(pkg.props.depends)
        if "plasma-workspace" in deps or "plasma-framework" in deps:
            return True
        return False


class ApplicationsWorker(Worker):

    def getAll(self):
        self.datas = render.get.all_repo_pkgs(self.title)

    def _includeItem(self, item, detail=False):
        icon = item.props.icon.replace('/usr/share/app-info/', '')
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
            'pkg': item.props.name,
            'name': item.props.app_name,
            'url': item.props.url,
            'icon': icon,
            'desc': item.props.desc,
        }
        if self.is_gtk(item):
            ret['gtk'] = 1
        if self.is_plasma(item):
            ret['plasma'] = 1
        if self.is_qt(item):
            ret['qt'] = 1
        return ret


class PackagesWorker(Worker):
    def getAll(self):
        self.datas = render.get.all_repo_pkgs(self.title)

    def _includeItem(self, item, detail=False):
        if detail:
            ret = {}
            for prop in item.props:
                key = prop.name
                value = item.get_property(prop.name)
                if key == "icon":
                    value = "images/package.svg"
                    if self.is_manjaro(item) == 1:
                        value = "images/logo.svg"
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
            'name': item.props.name,
            #'app_name': item.props.name,    # not exists
            'url': item.props.url,
            'icon': "images/package.svg",
            'desc': item.props.desc,
        }
        if self.is_gtk(item):
            ret['gtk'] = 1
        if self.is_plasma(item):
            ret['plasma'] = 1
        if self.is_qt(item):
            ret['qt'] = 1
        if self.is_manjaro(item) == 1:
            ret['icon'] = "images/logo.svg"
        return ret


class SnapWorker(Worker):
    def getAll(self):
        database = render.get.external_repos()[1]
        for category in render.get.external_repos()[0]:
            cat = database.get_category_snaps(category)
            for app in cat:
                self.datas.append(app)

    def _includeItem(self, item, detail=False):
        if detail:
            ret = {}
            for prop in item.props:
                value = item.get_property(prop.name)
                if value:
                    ret[prop.name] = value
            return ret
        return {
            'name': item.props.name,
            'url': item.props.url,
            'icon': item.props.icon,
            'desc': item.props.desc,
        }

    def getPackage(self, package_name):
        database = render.get.external_repos()[1]
        for category in render.get.external_repos()[0]:
            cat = database.get_category_snaps(category)
            for app in cat:
                if app.props.name == package_name:
                    self.datas.append(app)
                    return

'''
class CategoriesWorker(Worker):
    def getAll(self):
        self.datas = render.get_categories()

    def _includeItem(self, item):
        return item
'''
