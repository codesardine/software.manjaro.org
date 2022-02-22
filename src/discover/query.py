from discover import models


def last_updated():
    return models.Discover.query.with_entities(
        models.Discover.last_updated
    ).first()[0]

def apps():
    return models.Apps.query.order_by(models.Apps.title).all()

def packages():
    return models.Packages.query.all()

def snaps():
    return models.Snaps.query.order_by(models.Snaps.title).all()

def flatpaks():
    return models.Flatpaks.query.order_by(models.Flatpaks.title).all()

def app_by_name(name):
    return models.Apps.query.filter_by(name=name).first()

def pkg_by_name(name):
    return models.Packages.query.filter_by(name=name).first()

def snap_by_name(name):
    return models.Snaps.query.filter_by(name=name).first()

def flatpak_by_name(name):
    return models.Flatpaks.query.filter_by(name=name).first()

def snap_by_title(title):
    return models.Snaps.query.filter_by(title=title).first()

def flatpak_by_title(title):
    return models.Flatpaks.query.filter_by(title=title).first()
