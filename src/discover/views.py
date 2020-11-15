from discover import app, cache
import discover.render as render


@app.route("/")
@app.route("/applications/")
@cache.cached(timeout=50)
def applications():
    return render.pkgs_template(render.get_categories()[0].get("title"))


@app.route("/applications/<application>")
@cache.cached(timeout=40)
def application(application):
    return render.search_package_template(application, "Application")


@app.route("/packages/<package>")
@cache.cached(timeout=40)
def package(package):
    return render.search_package_template(package, "Package")


@app.route("/snaps/<snap>")
@cache.cached(timeout=40)
def snap(snap):
    return render.search_package_template(snap, "Snap")


@app.route("/flatpaks/<flatpak>")
@cache.cached(timeout=40)
def flatpak(flatpak):
    return render.search_package_template(flatpak, "Flatpak")
    

@app.route("/packages/")
@cache.cached(timeout=80)
def packages():
    return render.pkgs_template(render.get_categories()[1].get("title"))


@app.route("/snaps/")
@cache.cached(timeout=50)
def snaps():
    return render.external_repos_template(render.get_categories()[2].get("title"))


@app.route("/flatpaks/")
@cache.cached(timeout=50)
def flatpaks():
    return render.external_repos_template(render.get_categories()[3].get("title"))


#@app.route("/")
@cache.cached(timeout=40)
def featured():
    return render.appstream_template("Featured")


@app.route("/<error404>/")
@cache.cached(timeout=40)
def error_404(error404):
    return render.template_404()


@app.route('/sitemap.xml', methods=['GET'])
@cache.cached(timeout=100)
def sitemap():
    return render.sitemap_template()
