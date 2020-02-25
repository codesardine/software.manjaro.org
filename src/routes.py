from flask import Flask
import pamac
import utils
app = Flask(__name__)

# Repositorys
@app.route("/applications")
def applications():
    return utils.pkgs_template(utils.get_categories()[1].get("title"))


@app.route("/applications/<application>")
def application(application):
    return utils.search_package_template(application, "Native")


@app.route("/packages/<package>")
def package(package):
    return utils.search_package_template(package, "Native")


@app.route("/snaps/<snap>")
def snap(snap):
    return utils.search_package_template(snap, "Snap")


@app.route("/flatpaks/<flatpak>")
def flatpak(flatpak):
    print(flatpak)
    return utils.search_package_template(flatpak, "Flatpak")
    

@app.route("/packages")
def packages():
    return utils.pkgs_template(utils.get_categories()[2].get("title"))


@app.route("/snaps")
def snaps():
    return utils.external_repos_template(utils.get_categories()[3].get("title"))


@app.route("/flatpaks")
def flatpaks():
    return utils.external_repos_template(utils.get_categories()[4].get("title"))


#APPSTREAM
@app.route("/")
def featured():
    return utils.appstream_template(utils.get_categories()[0].get("title"))
