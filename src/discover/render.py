from flask import render_template
import discover.pamac as pamac

get = pamac.Get()


def get_categories():
    return {'title': 'Featured', 'href': ''},\
           {'title': 'Applications', 'href': 'applications'},\
           {'title': 'Packages', 'href': 'packages'},\
           {'title': 'Snaps', 'href': 'snaps'}, \
           {'title': 'Flatpaks', 'href': 'flatpaks'}


def get_appstream_app_list(category):
    return get.appstream_category(category)


def appstream_template(category):
    template = "featured.html"
    apps = get_appstream_app_list(category)
    return render_template(template, apps=apps, nav=get_categories(), title=category)


def pkgs_template(title):

    template = f"{title.lower()}.html"
    description = f"Discover {title.lower()} available on Manjaro linux."
    apps = get.all_repo_pkgs(title)
    return render_template(template, apps=apps, nav=get_categories(), title=title, total=len(apps), description=description)


def external_repos_template(title):

    template = f"{title.lower()}.html"
    description = f"Discover {title.lower()} available on Manjaro linux."
    categories = get.external_repos()[0]
    pamac_database = get.external_repos()[1]
    return render_template(template, categories=categories, nav=get_categories(), title=title, database=pamac_database, description=description)


def template_404():
    title = "YOU ARE LOST"
    return render_template('404.html', nav=get_categories(), title=title)


def search_package_template(pkg_name, pkg_format):

    pkg = get.search_single_package(pkg_name, pkg_format)
    if not pkg:
        return template_404()        

    title = pkg.get_app_name()
    if not title:
        title = pkg.get_name()

    description = pkg.get_desc()
    if not description:
        description = pkg.get_log_desc()

    template = f"single-{pkg_format.lower()}.html"
    return render_template(template, nav=get_categories(), pkg=pkg, title=title, pkg_format=pkg_format, description=description)
