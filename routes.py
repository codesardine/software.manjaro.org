from flask import Flask, render_template
app = Flask(__name__)


def get_category(category):
    import pamac
    return pamac.Get().category(category)


def template(category):
    nav = {'title': 'Featured', 'href': '/'}, {'title': 'Photo & Video', 'href': 'photo_and_video'},\
          {'title': 'Music & Audio', 'href': 'music_and_audio'}, {'title': 'Productivity', 'href': 'productivity'}, \
          {'title': 'Communication & News', 'href': 'communication_and_news'}, {'title': 'Games', 'href': 'games'},\
          {'title': 'Education & Science', 'href': 'education_and_science'}, \
          {'title': 'Utilities', 'href': 'utilities'}, {'title': 'Development', 'href': 'development'}
    return render_template("apps.html", apps=get_category(category), title=category, nav=nav)


@app.route("/")
def featured():
    category = "Featured"
    return template(category)


@app.route("/photo_and_video")
def photo_and_video():
    category = "Photo & Video"
    return template(category)


@app.route("/music_and_audio")
def music_and_audio():
    category = "Music & Audio"
    return template(category)


@app.route("/productivity")
def productivity():
    category = "Productivity"
    return template(category)


@app.route("/communication_and_news")
def communication_and_news():
    category = "Communication & News"
    return template(category)


@app.route("/education_and_science")
def education_and_science():
    category = "Education & Science"
    return template(category)


@app.route("/games")
def games():
    category = "Games"
    return template(category)


@app.route("/utilities")
def utilities():
    category = "Utilities"
    return template(category)


@app.route("/development")
def development():
    category = "Development"
    return template(category)
