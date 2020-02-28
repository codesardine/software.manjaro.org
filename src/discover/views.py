from discover import app, cache
import discover.render as render
import discover.api as api


@app.route("/applications/")
@cache.cached(timeout=50)
def applications():
    return render.pkgs_template(render.get_categories()[1].get("title"))


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
    return render.pkgs_template(render.get_categories()[2].get("title"))


@app.route("/snaps/")
@cache.cached(timeout=50)
def snaps():
    return render.external_repos_template(render.get_categories()[3].get("title"))


@app.route("/flatpaks/")
@cache.cached(timeout=50)
def flatpaks():
    return render.external_repos_template(render.get_categories()[4].get("title"))


@app.route("/")
@cache.cached(timeout=40)
def featured():
    return render.appstream_template(render.get_categories()[0].get("title"))


@app.route("/<error404>/")
@cache.cached(timeout=40)
def error_404(error404):
    return render.template_404()


@app.route('/sitemap.xml', methods=['GET'])
@cache.cached(timeout=100)
def sitemap():
    return render.sitemap_template()


# API

@app.route("/api/applications")
def api_applications():
    worker = api.ApplicationsWorker(1)
    worker.get_all()
    return worker.to_json()

@app.route("/api/applications/<pkgname>")
def api_application(pkgname):
    worker = api.ApplicationsWorker(1)
    worker.get_package(pkgname)
    return worker.to_json()

@app.route("/api/applications/filter", defaults={"option": "count"})
@app.route("/api/applications/filter/<option>")
def api_applications_filter(option=""):
    worker = api.ApplicationsWorker(1)
    worker.get_all()
    return worker.to_json(option)

@app.route("/api/packages")
def api_packages():
    worker = api.PackagesWorker(2)
    worker.get_all()
    return worker.to_json()

@app.route("/api/packages/<pkgname>")
def api_package(pkgname):
    worker = api.PackagesWorker(2)
    worker.get_package(pkgname)
    return worker.to_json()

@app.route("/api/packages/filter", defaults={"option": "count"})
@app.route("/api/packages/filter/<option>")
def api_packages_filter(option=""):
    """
    filter/option :
       - count : only count applications, items[] is empty
       - name : only string pkg.get_name() in items[]
       - app : only string pkg.get_app_name() in items[]
       - url@xxx : filter, "xxx" is in url
       - desc@xxx : filter, "xxx" is in description
       - dep@xxx : filter, "xxx" is a dependence
    """
    worker = api.PackagesWorker(1)
    worker.get_all()
    return worker.to_json(option)

@app.route("/api/snaps")
def api_snaps():
    worker = api.SnapWorker(2)
    worker.get_all()
    return worker.to_json()

@app.route("/api/snaps/<pkgname>")
def api_snap(pkgname):
    worker = api.SnapWorker(2)
<<<<<<< HEAD
    worker.getPackage(pkgname)
    return worker.toJson()
||||||| constructed merge base
    worker.getPackage(pkgname)
    return worker.toJson()
=======
    worker.get_package(pkgname)
    return worker.to_json()
>>>>>>> add filters
