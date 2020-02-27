from discover import app
import discover.render as render


@app.route("/applications/")
def applications():
    return render.pkgs_template(render.get_categories()[1].get("title"))


@app.route("/applications/<application>")
def application(application):
    return render.search_package_template(application, "Native")


@app.route("/packages/<package>")
def package(package):
    return render.search_package_template(package, "Native")


@app.route("/snaps/<snap>")
def snap(snap):
    return render.search_package_template(snap, "Snap")


@app.route("/flatpaks/<flatpak>")
def flatpak(flatpak):
    return render.search_package_template(flatpak, "Flatpak")
    

@app.route("/packages/")
def packages():
    return render.pkgs_template(render.get_categories()[2].get("title"))


@app.route("/snaps/")
def snaps():
    return render.external_repos_template(render.get_categories()[3].get("title"))


@app.route("/flatpaks/")
def flatpaks():
    return render.external_repos_template(render.get_categories()[4].get("title"))


@app.route("/")
def featured():
    return render.appstream_template(render.get_categories()[0].get("title"))


@app.route("/<error404>/")
def error_404(error404):
    return render.template_404()
