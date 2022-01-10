from discover import app, cache, query
from Manjaro.SDK import PackageManager
from flask import render_template, redirect, make_response, url_for, request
from datetime import date, timedelta
import json

def navigation():
    return {'title': 'Applications', 'href': '/applications'},\
           {'title': 'Snaps', 'href': '/snaps'}, \
           {'title': 'Flatpaks', 'href': '/flatpaks'}


@app.route("/maintenance")
def in_maintenance_mode():
    if app.config['IS_MAINTENANCE_MODE']:
        return render_template(
            "maintenance-mode.html",
            title="Software Center",
            nav=navigation(),
            description="Maintenance Mode"
            )
    else:
        return redirect("/", 301, Response=None)

@app.route("/")
def root():
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        return redirect("/applications", 302, Response=None)


@app.route("/applications")
@cache.cached(timeout=50)
def applications():
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        apps = query.apps()
        pkgs = query.packages()
        data = {}
        for p in apps:
            icon = p.icon.replace("//", "/")
            if icon:
                data[p.name] = f"{ icon }"
            else:
                data[p.name] = "static/images/package.svg"

        for p in pkgs:
            data[p.name] = "static/images/package.svg"
            
        return render_template(
            "applications.html",
            updated=query.last_updated(),
            apps=apps,
            data=json.dumps(data),
            title="Software Center",
            nav=navigation(),
            description="View, Search or install Software independently of packaging format."
            )


@app.route("/package/<name>")
@cache.cached(timeout=40)
def package(name):
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        p = query.pkg_by_name(name)
        a = query.app_by_name(name)
        if a is not None:
            pkg = a
        elif p is not None:
            pkg = p

        if a or p is not None:
            if not hasattr(pkg, "screenshots") or not pkg.screenshots:
                pkg.screenshots = None
            pkg.optdepends = json.loads(pkg.optdepends)
            return render_template(
                "single-package.html",
                updated=query.last_updated(),
                pkg=pkg,
                title=pkg.name,
                nav=navigation(),
                description=pkg.description
            )
        else:
            return redirect("/", 302, Response=None)


@app.route("/snap/<name>")
@cache.cached(timeout=40)
def snap(name):
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        pkg = query.snap_by_name(name)
        if not hasattr(pkg, "screenshots") or not pkg.screenshots:
                pkg.screenshots = None
        return render_template(
            "single-package.html",
            updated=query.last_updated(),
            pkg=pkg,
            title=pkg.title,
            nav=navigation(),
            description=pkg.description
        )


@app.route("/flatpak/<name>")
@cache.cached(timeout=40)
def flatpak(name):
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        pkg = query.flatpak_by_name(name)
        if not hasattr(pkg, "screenshots") or not pkg.screenshots:
                pkg.screenshots = None
        return render_template(
            "single-package.html",
            updated=query.last_updated(),
            pkg=pkg,
            title=pkg.title,
            nav=navigation(),
            description=pkg.description
        )


@app.route("/snaps")
@cache.cached(timeout=50)
def snaps():
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        apps = query.snaps()
        data = {}
        for p in apps:
            icon = p.icon
            if icon:
                data[p.name] = f"{ icon }"
            else:
                data[p.name] = "static/images/package.svg"

        return render_template(
            "applications.html",
            updated=query.last_updated(),
            apps=apps,
            data=json.dumps(data),
            title="Snaps",
            nav=navigation(),
            description="Explore snaps available in Manjaro linux."
        )


@app.route("/flatpaks")
@cache.cached(timeout=50)
def flatpaks():
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        apps = query.flatpaks()
        data = {}
        for p in apps:
            icon = p.icon
            if icon:
                data[p.name] = f"{ icon }"
            else:
                data[p.name] = "static/images/package.svg"

        return render_template(
            "applications.html",
            updated=query.last_updated(),
            apps=apps,
            data=json.dumps(data),
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
    if app.config['IS_MAINTENANCE_MODE']: 
        return redirect("/maintenance", 302, Response=None)
    else:
        thirty_days = (date.today() - timedelta(days=30)).isoformat()
        urls = [("https://discover.manjaro.org/applications", thirty_days),
                ("https://discover.manjaro.org/snaps", thirty_days),
                ("https://discover.manjaro.org/flatpaks", thirty_days)
        ]

        for pkg in query.apps():
            urls.append(
                (f"https://discover.manjaro.org/package/{pkg.name}",
                thirty_days)
                )

        for pkg in query.packages():
            urls.append(
                (f"https://discover.manjaro.org/package/{pkg.name}",
                thirty_days)
                )

        for pkg in query.snaps():
            urls.append(
                (f"https://discover.manjaro.org/snap/{pkg.name}",
                thirty_days)
            )

        for pkg in query.flatpaks():
            urls.append(
                (f"https://discover.manjaro.org/flatpak/{pkg.name}",
                thirty_days)
            )

        
        response = make_response(
            render_template('sitemap_template.xml', urls=urls)
        )
        response.headers["Content-Type"] = "application/xml"
        return response
