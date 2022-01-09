from Manjaro.SDK import PackageManager
from discover import models, sql
from time import strftime
import json
# test sync behavior

class Database():
    def __init__(self):
        self.pamac = PackageManager.Pamac()

    def reload_tables(self):
        self.populate_pkg_tables()
        self.populate_flatpak_tables()
        self.populate_snap_tables()
        update_time = strftime("%Y-%m-%d %H:%M")
        sql.session.add(
            models.Discover(
                last_updated=update_time
            )
        )
        sql.drop_all()
        sql.create_all()
        sql.session.commit()  

    def populate_pkg_tables(self):        
        for pkg in self.pamac.get_all_pkgs():
            d = self.pamac.get_pkg_details(
                pkg.get_name()
            )
            if d["icon"]:
                model = models.Apps(
                    pkg_format="pamac",
                    app_id=d["app_id"],
                    icon=d["icon"].replace('/usr/share/app-info', '/static'),
                    launchable=d["launchable"],
                    title=d["title"],
                    backups=" ".join(d["backups"]),
                    build_date=d["build_date"],
                    check_depends=" ".join(d["check_depends"]),
                    conflits=" ".join(d["conflits"]),
                    depends=" ".join(d["depends"]),
                    description=d["description"],
                    download_size=d["download_size"],
                    groups=" ".join(d["groups"]),
                    ha_signature=d["ha_signature"],
                    pkg_id=d["pkg_id"],
                    install_date=d["install_date"],
                    installed_size=d["installed_size"],
                    installed_version=d["installed_version"],
                    license=d["license"],
                    long_description=d["long_description"],
                    makedepends=" ".join(d["makedepends"]),
                    name=d["name"],
                    optdepends=json.dumps(d["optdepends"]),
                    optionalfor=" ".join(d["optionalfor"]),
                    packager=d["packager"],
                    provides=" ".join(d["provides"]),
                    reason=d["reason"],
                    replaces=" ".join(d["replaces"]),
                    repository=d["repository"],
                    required_by=" ".join(d["required_by"]),
                    screenshots=" ".join(d["screenshots"]),
                    url=d["url"],
                    version=d["version"]
                )

            else:
                model = models.Packages(
                    pkg_format="pamac",
                    app_id=d["app_id"],
                    launchable=d["launchable"],
                    backups=" ".join(d["backups"]),
                    build_date=d["build_date"],
                    check_depends=" ".join(d["check_depends"]),
                    conflits=" ".join(d["conflits"]),
                    depends=" ".join(d["depends"]),
                    description=d["description"],
                    download_size=d["download_size"],
                    groups=" ".join(d["groups"]),
                    ha_signature=d["ha_signature"],
                    pkg_id=d["pkg_id"],
                    install_date=d["install_date"],
                    installed_size=d["installed_size"],
                    installed_version=d["installed_version"],
                    license=d["license"],
                    long_description=d["long_description"],
                    makedepends=" ".join(d["makedepends"]),
                    name=d["name"],
                    optdepends=json.dumps(d["optdepends"]),
                    optionalfor=" ".join(d["optionalfor"]),
                    packager=d["packager"],
                    provides=" ".join(d["provides"]),
                    reason=d["reason"],
                    replaces=" ".join(d["replaces"]),
                    repository=d["repository"],
                    required_by=" ".join(d["required_by"]),
                    url=d["url"],
                    version=d["version"]
                )

            sql.session.add(model)

    
    def populate_snap_tables(self):
        for pkg in self.pamac.get_all_snaps():
            d = self.pamac.get_snap_details(
                pkg.get_name()
            )
            sql.session.add(
                models.Snaps(
                    pkg_format="snap",
                    app_id=d["app_id"],
                    icon=d["icon"],
                    launchable=d["launchable"],
                    title=d["title"],
                    description=d["description"],
                    download_size=d["download_size"],
                    install_date=d["install_date"],
                    installed_size=d["installed_size"],
                    installed_version=d["installed_version"],
                    license=d["license"],
                    long_description=d["long_description"],
                    name=d["name"],
                    repository=" ".join(d["repository"]),
                    screenshots=" ".join(d["screenshots"]),
                    url=d["url"],
                    version=d["version"],
                    channel=d["channel"],
                    channels=" ".join(d["channels"]),
                    confined=d["confined"],
                    publisher=d["publisher"]
                    )
            )


    def populate_flatpak_tables(self):
        for pkg in self.pamac.get_all_flatpaks():
            d = self.pamac.get_flatpak_details(pkg)
            if d["icon"]:
                d["icon"] = d["icon"].replace(
                    "/var/lib/flatpak/appstream/flathub/x86_64/active/icons",
                    "/static/flatpak-icons"
                )
            sql.session.add(
                models.Flatpaks(
                    pkg_format="flatpak",
                    icon=d["icon"],
                    launchable=d["launchable"],
                    title=d["title"],
                    description=d["description"],
                    download_size=d["download_size"],
                    install_date=d["install_date"],
                    installed_size=d["installed_size"],
                    installed_version=d["installed_version"],
                    license=d["license"],
                    long_description=d["long_description"],
                    name=d["name"],
                    repository=" ".join(d["repository"]),
                    screenshots=" ".join(d["screenshots"]),
                    url=d["url"],
                    version=d["version"]
                )
            )
