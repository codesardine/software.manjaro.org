from Manjaro.SDK import PackageManager, Utils
from discover import models, sql, app
from time import strftime
from sqlalchemy.exc import IntegrityError
import json


class Database():
    def __init__(self):
        self.pamac = PackageManager.Pamac()
        self.package_icon = "/static/images/package.svg"

    def reload_tables(self):
        sql.drop_all()
        sql.create_all()
        sql.session.add(
            models.Discover(
                last_updated=strftime("%Y-%m-%d %H:%M")
            )
        )
        try:
            sql.session.commit()
        except IntegrityError:
            sql.session.rollback()
        finally:
            sql.session.close()
        self.populate_appimage_tables()
        app.config['IS_MAINTENANCE_MODE_APPIMAGES'] = False
        self.populate_pkg_tables()
        app.config['IS_MAINTENANCE_MODE_PKGS'] = False
        self.populate_flatpak_tables()
        app.config['IS_MAINTENANCE_MODE_FLATPAKS'] = False
        self.populate_snap_tables()
        app.config['IS_MAINTENANCE_MODE_SNAPS'] = False
      

    def populate_pkg_tables(self):   
        ignore_list = (
            "picom",
            "pantheon-onboarding",
            "wingpanel",
            "systemsettings",
            "kshutdown",
            "khelpcenter",
            "kinfocenter",
            "gnome-control-center",
            "discover",
            "deepin-control-center",
            "lxappearance-gtk3"
        )     
        for pkg in self.pamac.get_all_pkgs():
            d = self.pamac.get_pkg_details(
                pkg.get_name()
            )
            if d["icon"] and d["name"] not in ignore_list:
                model = models.Apps(
                    format="package",
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
                    format="package",
                    app_id=d["app_id"],
                    icon=self.package_icon,
                    launchable=d["launchable"],
                    backups=" ".join(d["backups"]),
                    build_date=d["build_date"],
                    check_depends=" ".join(d["check_depends"]),
                    conflits=" ".join(d["conflits"]),
                    depends=" ".join(d["depends"]),
                    description=d["description"],
                    download_size=d["download_size"],
                    groups=" ".join(d["groups"]),
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
            try:
                sql.session.commit()
            except IntegrityError:
                sql.session.rollback()
            finally:
                sql.session.close()

    
    def populate_snap_tables(self):
        for pkg in self.pamac.get_all_snaps():
            try:
                d = self.pamac.get_snap_details(
                    pkg.get_name()
                )
                if not d["icon"]:
                    d["icon"] = "/static/images/package.svg"
                sql.session.add(
                    models.Snaps(
                        format="snap",
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
                        repository=d["repository"],
                        screenshots=" ".join(d["screenshots"]),
                        url=d["url"],
                        version=d["version"],
                        channel=d["channel"],
                        channels=" ".join(d["channels"]),
                        confined=d["confined"],
                        publisher=d["publisher"]
                        )
                )
                try:
                    sql.session.commit()
                except IntegrityError:
                    sql.session.rollback()
                finally:
                    sql.session.close()
            except KeyError:
                pass

    
    def populate_flatpak_tables(self):
        for pkg in self.pamac.get_all_flatpaks():
            d = self.pamac.get_flatpak_details(pkg)
            if d["icon"]:
                d["icon"] = d["icon"].replace(
                    "/var/lib/flatpak/appstream/flathub/x86_64/active/icons",
                    "/static/flatpak-icons"
                )
            else:
                d["icon"] = self.package_icon
            sql.session.add(
                models.Flatpaks(
                    format="flatpak",
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
                    repository=d["repository"],
                    screenshots=" ".join(d["screenshots"]),
                    url=d["url"],
                    version=d["version"]
                )
            )
            try:
                sql.session.commit()
            except IntegrityError:
                sql.session.rollback()
            finally:
                sql.session.close()


    def populate_appimage_tables(self):
        from discover.appimage import appimages
        for d in appimages(): 
            if not d["icon"]:
                d["icon"] = self.package_icon        
            sql.session.add(
                models.Appimages(
                    format="appimage",
                    icon=d["icon"],
                    title=d["title"],
                    description=d["description"],
                    license=d["license"],
                    name=d["name"],
                    screenshots=" ".join(d["screenshots"]),
                    url=d["url"],
                    version=d["version"],
                    repository=d["repository"]
                )
            )
            try:
                sql.session.commit()
            except IntegrityError:
                sql.session.rollback()
            finally:
                sql.session.close()
