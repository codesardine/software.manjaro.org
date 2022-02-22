from urllib.request import urlopen
import json, re


def get_appimage(provider):
    response = urlopen(provider + "/feed.json")
    if response.status == 200:
        data = json.loads(response.read())
        items = data["items"]
        return items


def strip_html(html):
    regex = re.compile('<.*?>')
    text = re.sub(regex, '', html)
    return text


def appimages():
    data_url = "https://raw.githubusercontent.com/AppImage/appimage.github.io/master/database/"
    git_url = "https://github.com/"
    provider = "https://appimage.github.io"
    appimage = []
    for app in get_appimage(provider):
        app_data = {}
        try:
            links = app["links"]
            if app["license"]:
                app_data["license"] = app["license"]
            else:
                app_data["license"] = None

            app_data["name"] = links[0]["url"].replace("/", ".")
            app_data["version"] = None
            app_data["url"] = git_url + links[0]["url"] + "/releases"
            app_data["format"] = "appimage"
            app_data["repository"] = "https://github.com/AppImage/appimage.github.io"
            app_data["title"] = app["name"].replace("_", " ").replace(".", " ").replace("-", " ")
            
            try:
                app_data["description"] = strip_html(app["description"])
            except KeyError:
                app_data["description"] = "No description available"
            
            try:
                screenshots = []
                for img in app["screenshots"]:
                    if not img.startswith("http"):
                        img = data_url + img
                    screenshots.append(img)

                app_data["screenshots"] = screenshots
            except (KeyError, TypeError):
                app_data["screenshots"] = ""

            try:
                app_data["icon"] = data_url + app["icons"][0]
            except TypeError:
                app_data["icon"] = None

            appimage.append(app_data)
        except (TypeError, KeyError):
            pass
    return appimage