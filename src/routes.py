from flask import Flask
import pamac
import utils
app = Flask(__name__)
# Repositorys
#@app.route("/extra")
def extra():
    return utils.repository_template(utils.get_categories()[10].get("title"))


#@app.route("/community")
def community():
    return utils.repository_template(utils.get_categories()[11].get("title"))

#@app.route("/manjaro")
def manjaro():
    return utils.pkgs_template(utils.get_categories()[9].get("title"))

@app.route("/packages")
def packages():
    return utils.pkgs_template(utils.get_categories()[9].get("title"))


# appstream
@app.route("/")
def featured():
    return utils.appstream_template(utils.get_categories()[0].get("title"))


@app.route("/photo_and_video")
def photo_and_video():
    return utils.appstream_template(utils.get_categories()[1].get("title"))


@app.route("/music_and_audio")
def music_and_audio():
    return utils.appstream_template(utils.get_categories()[2].get("title"))


@app.route("/productivity")
def productivity():
    return utils.appstream_template(utils.get_categories()[3].get("title"))


@app.route("/communication_and_news")
def communication_and_news():
    return utils.appstream_template(utils.get_categories()[4].get("title"))


@app.route("/education_and_science")
def education_and_science():
    return utils.appstream_template(utils.get_categories()[5].get("title"))


@app.route("/games")
def games():
    return utils.appstream_template(utils.get_categories()[6].get("title"))


@app.route("/utilities")
def utilities():
    return utils.appstream_template(utils.get_categories()[7].get("title"))


@app.route("/development")
def development():
    return utils.appstream_template(utils.get_categories()[8].get("title"))
