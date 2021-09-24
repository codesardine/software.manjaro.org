from discover import app, cache, query
from Manjaro.SDK import PackageManager
from flask import render_template, redirect, make_response
from datetime import date, timedelta

def navigation():
    return {'title': 'Applications', 'href': 'applications'},\
           {'title': 'Snaps', 'href': 'snaps'}, \
           {'title': 'Flatpaks', 'href': 'flatpaks'}


@app.route("/")
def root():
    return render_template(
        "home.html",
        title="pick a format",
        nav=navigation(),
        description="Explore and install software available in Manjaro,  it supports native packages, Flatpaks and Snaps."
        )


@app.route("/applications")
@cache.cached(timeout=50)
def applications():
    return render_template(
        "applications.html",
        updated=query.pkg_last_updated(),
        apps=query.all_apps(),
        title="Applications",
        nav=navigation(),
        description="Explore native software in Manjaro."
    )


@app.route("/application/<name>")
@cache.cached(timeout=40)
def application(name):
    pkg = query.app_by_name(name)
    return render_template(
        "single-application.html",
        pkg=pkg,
        title=pkg.title,
        description=pkg.description)


@app.route("/package/<name>")
@cache.cached(timeout=40)
def package(name):
    p = query.pkg_by_name(name)
    a = query.app_by_name(name)
    if a is not None:
        pkg = a
    elif p is not None:
        pkg = p

    if a or p is not None:
        return render_template(
            "single-package.html",
            pkg=pkg,
            title=pkg.name,
            description=pkg.description
        )
    else:
        return redirect("/", 302, Response=None)


@app.route("/snap/<name>")
@cache.cached(timeout=40)
def snap(name):
    pkg = query.snap_by_name(name)
    return render_template(
        "single-snap.html",
        pkg=pkg,
        title=pkg.title,
        description=pkg.description
    )


@app.route("/flatpak/<name>")
@cache.cached(timeout=40)
def flatpak(name):
    pkg = query.flatpak_by_name(name)
    return render_template(
        "single-flatpak.html",
        pkg=pkg,
        title=pkg.title,
        description=pkg.description
    )


@app.route("/snaps")
@cache.cached(timeout=50)
def snaps():
    return render_template(
        "snaps.html",
        updated=query.snap_last_updated(),
        apps=query.all_snaps(),
        title="Snaps",
        nav=navigation(),
        description="Explore snaps available in Manjaro linux."
    )


@app.route("/flatpaks")
@cache.cached(timeout=50)
def flatpaks():
    return render_template(
        "flatpaks.html",
        updated=query.flatpak_last_updated(),
        apps=query.all_flatpaks(),
        title="Flatpaks",
        nav=navigation(),
        description="Explore flatpaks available in Manjaro linux."
    )


@app.route("/<error404>")
@cache.cached(timeout=40)
def error_404(error404):
    return redirect("/", 302, Response=None)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    thirty_days = (date.today() - timedelta(days=30)).isoformat()
    urls = [("https://discover.manjaro.org/applications", thirty_days),
            ("https://discover.manjaro.org/snaps", thirty_days),
            ("https://discover.manjaro.org/flatpaks", thirty_days)
    ]

    for pkg in query.all_apps():
        urls.append(
            (f"https://discover.manjaro.org/application/{pkg.name}",
             thirty_days)
            )

    for pkg in query.all_snaps():
        urls.append(
            (f"https://discover.manjaro.org/snap/{pkg.name}",
             thirty_days)
        )

    for pkg in query.all_flatpaks():
        urls.append(
            (f"https://discover.manjaro.org/flatpak/{pkg.name}",
             thirty_days)
        )

    
    response = make_response(
        render_template('sitemap_template.xml', urls=urls)
    )
    response.headers["Content-Type"] = "application/xml"
    return response
