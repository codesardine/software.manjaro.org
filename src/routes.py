from flask import Flask, render_template
app = Flask(__name__)

import pamac
get = pamac.Get ()

def get_categories():
    return {'title': 'Featured', 'href': '/'},\
           {'title': 'Photo & Video', 'href': 'photo_and_video'},\
           {'title': 'Music & Audio', 'href': 'music_and_audio'},\
           {'title': 'Productivity', 'href': 'productivity'},\
           {'title': 'Communication & News', 'href': 'communication_and_news'},\
           {'title': 'Education & Science', 'href': 'education_and_science'},\
           {'title': 'Games', 'href': 'games'},\
           {'title': 'Utilities', 'href': 'utilities'},\
           {'title': 'Development', 'href': 'development'}


def get_appstream_app_list(category):
    return get.category(category)


def template(category):
    if category == "Featured":
        template = "featured.html"
    else:
        template = "apps.html"
    return render_template(template, apps=get_appstream_app_list(category), nav=get_categories(), title=category)


@app.route("/")
def featured():
    return template(get_categories()[0].get("title"))


@app.route("/photo_and_video")
def photo_and_video():
    return template(get_categories()[1].get("title"))


@app.route("/music_and_audio")
def music_and_audio():
    return template(get_categories()[2].get("title"))


@app.route("/productivity")
def productivity():
    return template(get_categories()[3].get("title"))


@app.route("/communication_and_news")
def communication_and_news():
    return template(get_categories()[4].get("title"))


@app.route("/education_and_science")
def education_and_science():
    return template(get_categories()[5].get("title"))


@app.route("/games")
def games():
    return template(get_categories()[6].get("title"))


@app.route("/utilities")
def utilities():
    return template(get_categories()[7].get("title"))


@app.route("/development")
def development():
    return template(get_categories()[8].get("title"))

