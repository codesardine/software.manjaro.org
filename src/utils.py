from flask import render_template
import pamac
get = pamac.Get()

def get_categories():
    return {'title': 'Featured', 'href': '/'},\
           {'title': 'Applications', 'href': 'applications'},\
           {'title': 'Packages', 'href': 'packages'},\
           {'title': 'Snaps', 'href': 'snaps'}

           #{'title': 'Photo & Video', 'href': 'photo_and_video'},\
           #{'title': 'Music & Audio', 'href': 'music_and_audio'},\
           #{'title': 'Productivity', 'href': 'productivity'},\
           #{'title': 'Communication & News', 'href': 'communication_and_news'},\
           #{'title': 'Education & Science', 'href': 'education_and_science'},\
           #{'title': 'Games', 'href': 'games'},\
           #{'title': 'Utilities', 'href': 'utilities'},\
           #{'title': 'Development', 'href': 'development'},\                     
           #{'title': 'Manjaro', 'href': 'manjaro'}
           #{'title': 'Extra', 'href': 'extra'},\
           #{'title': 'Community', 'href': 'communnity'}
           


def get_appstream_app_list(category):
    return get.appstream_category(category)


def get_repo_pkg_list(repo):
    return get.individual_repo_pkgs(repo)


def appstream_template(category):
    if category == "Featured":
        template = "featured.html"
    else:
        template = "appstream.html"
    apps = get_appstream_app_list(category)
    return render_template(template, apps=apps, nav=get_categories(), title=category)


def repository_template(repo):
    return render_template("repository.html", pkgs=get_repo_pkg_list(repo), title=repo)

def pkgs_template(title):
    if title == "Applications":
        template = "applications.html"
    else:
        template = "packages.html"
    apps = get.all_repo_pkgs(title)
    return render_template(template, apps=apps, nav=get_categories(), title=title, total=len(apps))

def snaps_template(title):
    snap_categories = get.all_snaps()[0]
    pamac_database = get.all_snaps()[1]
    return render_template("snaps.html", categories=snap_categories, nav=get_categories(), title=title, database=pamac_database)