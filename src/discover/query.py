from discover.database import Database
from discover import models


def pkg_last_updated():
    return models.Discover.query.with_entities(
        models.Discover.pkg_last_updated
    ).one()[0]

def snap_last_updated():
    return models.Discover.query.with_entities(
        models.Discover.snap_last_updated
    ).one()[0]

def flatpak_last_updated():
    return models.Discover.query.with_entities(
        models.Discover.flatpak_last_updated
    ).one()[0]

def all_apps():
    return models.Apps.query.all()

def all_snaps():
    return models.Snaps.query.all()

def all_flatpaks():
    return models.Flatpaks.query.all()

def app_by_name(name):
    return models.Apps.query.filter_by(name=name).first()

def pkg_by_name(name):
    return models.Packages.query.filter_by(name=name).first()

def snap_by_name(name):
    return models.Snaps.query.filter_by(name=name).first()

def flatpak_by_name(name):
    return models.Flatpaks.query.filter_by(name=name).first()
