from flask import render_template
import pamac

def get_categories():
    return {'title': 'Featured', 'href': '/'},\
           {'title': 'Photo & Video', 'href': 'photo_and_video'},\
           {'title': 'Music & Audio', 'href': 'music_and_audio'},\
           {'title': 'Productivity', 'href': 'productivity'},\
           {'title': 'Communication & News', 'href': 'communication_and_news'},\
           {'title': 'Education & Science', 'href': 'education_and_science'},\
           {'title': 'Games', 'href': 'games'},\
           {'title': 'Utilities', 'href': 'utilities'},\
           {'title': 'Development', 'href': 'development'}#,\
           #{'title': 'Extra', 'href': 'extra'},\
           #{'title': 'Community', 'href': 'communnity'}


def get_appstream_app_list(category):
    return pamac.Get().appstream_category(category)


def get_repo_pkg_list(repo):
    return pamac.Get().repo(repo)


def appstream_template(category):
    if category == "Featured":
        template = "featured.html"
    else:
        template = "applications.html"
    return render_template(template, apps=get_appstream_app_list(category), nav=get_categories(), title=category)


def repository_template(repo):
    return render_template("repository.html", pkgs=get_repo_pkg_list(repo), title=repo)