from discover import app, query
from flask import render_template, redirect, make_response, jsonify, request
from datetime import date, timedelta
import json, re
from flask_caching import Cache
from discover.templates.filters import truncate_description as td

cache = Cache(app, config={
    "CACHE_TYPE": "filesystem",
    'CACHE_DIR': './data/cache',
    "CACHE_DEFAULT_TIMEOUT": 3600
})

def navigation():
    return {'title': 'Applications', 'href': '/applications'},\
           {'title': 'Snaps', 'href': '/snaps'}, \
           {'title': 'Flatpaks', 'href': '/flatpaks'}, \
           {'title': 'Appimages', 'href': '/appimages'}

def save_record(url, title, description, _type, pkg):
        return {
        "url": url,
        "title": title,
        "description": re.sub(' {2,}', ' ', td(description.replace("\n", ""), 160)),
        "is_doc": False,
        "type": _type,
        "package": pkg
        }

@app.route("/")
def root():
     return redirect("/applications", 302, Response=None)

@app.route("/search.json")
def search():
    search_query = request.args.get('query', None)
    if search_query:
        _type = request.args.get('type', None)
        providers = []
        if _type:
            type_results = []
            pkg_type = _type.split(" ")
            for _format in pkg_type:
                if _format == "appimage":
                    providers.append(query.appimages())
                if _format == "package":
                    providers.append(query.apps())
                    providers.append(query.packages())
                if _format == "flatpak":
                    providers.append(query.flatpaks())
                if _format == "snap":
                    providers.append(query.snaps())
        else:
            providers.append(query.appimages())
            providers.append(query.flatpaks())
            providers.append(query.snaps())
            providers.append(query.apps())
            providers.append(query.packages())

        search_results = []
        for provider in providers:
            for item in provider:
                url = f"https://software.manjaro.org/{item.format}/"
                if not item.description:
                    item.description = "No description available"
                if not item.title:
                    item.title = item.name        
                    
                search_fields = " ".join([item.name, item.title, item.description])
                matches = []
                terms = search_query.split(" ")
                words = search_fields.split(" ")
                for word in words:
                    for term in terms:
                        if term == word.lower():
                            matches.append(True)
                        else:
                            matches.append(False)
                
                # one term match
                if len(matches) == len(words) and True in matches:
                    search_results.append(
                        save_record(
                            f"{url}{item.name}", item.title, item.description, item.format, item.name
                        )
                    )

                # multiple terms match
                elif len(terms) > 1:
                    word_match = 0
                    for match in matches:
                        if match:
                            word_match += 1
                    if word_match > len(terms):
                        search_results.append(
                        save_record(
                            f"{url}{item.name}", item.title, item.description, item.format, item.name
                        )
                    )

        return jsonify(search_results)

@app.route("/applications")
@cache.cached(timeout=50)
def applications():
    apps = query.apps()
    pkgs = query.packages()
    data = {}
    for p in apps:
        #TODO move screenshot search to database
        if not p.screenshots:
            f = query.flatpak_by_title(p.title)
            if f is not None and f.screenshots:
                p.screenshots = f.screenshots
            else:
                s = query.snap_by_title(p.title)
                if s is not None and s.screenshots:
                    p.screenshots = s.screenshots

    for p in pkgs:
        data[p.name] = f"{ p.icon }"
        
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
    apps = query.snaps()
    return render_template(
        "applications.html",
        updated=query.last_updated(),
        apps=apps,
        title="Snaps",
        nav=navigation(),
        description="Explore snaps available in Manjaro linux."
    )


@app.route("/flatpaks")
@cache.cached(timeout=50)
def flatpaks():
    apps = query.flatpaks()
    return render_template(
        "applications.html",
        updated=query.last_updated(),
        apps=apps,
        title="Flatpaks",
        nav=navigation(),
        description="Explore flatpaks available in Manjaro linux."
    )


@app.route("/appimages")
@cache.cached(timeout=50)
def appimages():
    apps = query.appimages()    
    return render_template(
        "applications.html",
        updated=query.last_updated(),
        apps=apps,
        title="Appimage",
        nav=navigation(),
        description="Explore Appimages available in Manjaro linux."
    )


@app.route("/appimage/<name>")
@cache.cached(timeout=40)
def appimage(name): 
    pkg = query.appimage_by_name(name)
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


@app.route("/<error404>")
@cache.cached(timeout=40)
def error_404(error404):
    return redirect("/", 302, Response=None)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    thirty_days = (date.today() - timedelta(days=30)).isoformat()
    urls = [("https://software.manjaro.org/applications", thirty_days),
            ("https://software.manjaro.org/snaps", thirty_days),
            ("https://software.manjaro.org/flatpaks", thirty_days),
            ("https://software.manjaro.org/appimages", thirty_days)
    ]

    for pkg in query.apps():
        urls.append(
            (f"https://software.manjaro.org/package/{pkg.name}",
            thirty_days)
            )

    for pkg in query.packages():
        urls.append(
            (f"https://software.manjaro.org/package/{pkg.name}",
            thirty_days)
            )

    for pkg in query.snaps():
        urls.append(
            (f"https://software.manjaro.org/snap/{pkg.name}",
            thirty_days)
        )

    for pkg in query.flatpaks():
        urls.append(
            (f"https://software.manjaro.org/flatpak/{pkg.name}",
            thirty_days)
        )

    for pkg in query.appimages():
        urls.append(
            (f"https://software.manjaro.org/appimage/{pkg.name}",
            thirty_days)
        )

    
    response = make_response(
        render_template('sitemap_template.xml', urls=urls)
    )
    response.headers["Content-Type"] = "application/xml"
    return response
