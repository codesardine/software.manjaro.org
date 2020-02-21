from flask import Flask
from functools import lru_cache as cache
import pamac
import utils
app = Flask(__name__)

# Repositorys
@app.route("/applications")
@cache(maxsize=32)
def applications():
    return utils.pkgs_template(utils.get_categories()[1].get("title"))
    

@app.route("/packages")
@cache(maxsize=64)
def packages():
    return utils.pkgs_template(utils.get_categories()[2].get("title"))


@app.route("/snaps")
@cache(maxsize=32)
def snaps():
    return utils.external_repos_template(utils.get_categories()[3].get("title"))


@app.route("/flatpaks")
@cache(maxsize=32)
def flatpaks():
    return utils.external_repos_template(utils.get_categories()[4].get("title"))


#APPSTREAM
@app.route("/")
@cache(maxsize=24)
def featured():
    return utils.appstream_template(utils.get_categories()[0].get("title"))
