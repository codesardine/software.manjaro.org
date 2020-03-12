from discover import database


class Get:
       
    @staticmethod
    def appstream_category(category):
        return database.get_category_pkgs(category)

    @staticmethod
    def all_repo_pkgs(title):
        pkgs = []
        for repository in database.get_repos_names():
            iter_obj = iter(database.get_repo_pkgs(repository))
            if title == "Packages":
                while 1:
                    try:
                        package = next(iter_obj)
                        icon = package.get_icon()
                        if not icon:
                            pkgs.append(package)
                    except StopIteration:
                        break

            elif title == "Applications":
                while 1:
                    try:
                        package = next(iter_obj)
                        icon = package.get_icon()
                        if icon:
                            pkgs.append(package)
                    except StopIteration:
                        break
                
        return tuple(pkgs)

    @staticmethod
    def external_repos():
        # FIXME some unknown categories are missing
        categories = database.get_categories_names()
        return categories, database

    @staticmethod
    def search_single_package(pkg_name, pkg_format):

        if pkg_format == "Package" or pkg_format == "Application":
            repo = database.search_repos_pkgs(pkg_name)

        elif pkg_format == "Snap":
            repo = database.search_snaps(pkg_name)

        elif pkg_format == "Flatpak":
            repo = database.search_flatpaks(pkg_name)

        for pkg in repo:
            if pkg_name == pkg.get_name():
                return pkg

        return None

def preload():
    return Get.all_repo_pkgs("Packages")

packages = preload()

