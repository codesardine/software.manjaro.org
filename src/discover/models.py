from discover import sql


class ScreenshotsTemplate:
    screenshots = sql.Column(sql.String(150), nullable=True)
    

class BaseTemplate:
    id                = sql.Column(sql.Integer, primary_key=True)
    pkg_format        = sql.Column(sql.String(20), nullable=False)
    app_id            = sql.Column(sql.String(100), nullable=True)
    icon              = sql.Column(sql.String(110), nullable=True)
    title             = sql.Column(sql.String(100), nullable=True)
    description       = sql.Column(sql.String(250), nullable=True)
    download_size     = sql.Column(sql.Integer, nullable=True)
    install_date      = sql.Column(sql.String(20), nullable=True)
    installed_size    = sql.Column(sql.String(20), nullable=True)
    installed_version = sql.Column(sql.String(20), nullable=True)
    launchable        = sql.Column(sql.String(100), nullable=True)
    license           = sql.Column(sql.String(30), nullable=True)
    long_description  = sql.Column(sql.String(450), nullable=True)
    name              = sql.Column(sql.String(20), unique=True)
    repository        = sql.Column(sql.String(100), nullable=True)
    url               = sql.Column(sql.String(150), nullable=True)
    version           = sql.Column(sql.String(20), nullable=True)


class PackageTemplate(BaseTemplate):
    pkg_id        = sql.Column(sql.String(100), nullable=True)
    backups       = sql.Column(sql.String(150), nullable=True)
    build_date    = sql.Column(sql.String(150), nullable=True)
    check_depends = sql.Column(sql.String(150), nullable=True)
    conflits      = sql.Column(sql.String(150), nullable=True)
    depends       = sql.Column(sql.String(150), nullable=True)
    groups        = sql.Column(sql.String(150), nullable=True)
    ha_signature  = sql.Column(sql.String(150), nullable=True)
    makedepends   = sql.Column(sql.String(150), nullable=True)
    optdepends    = sql.Column(sql.String(150), nullable=True)
    optionalfor   = sql.Column(sql.String(150), nullable=True)
    packager      = sql.Column(sql.String(150), nullable=True)
    provides      = sql.Column(sql.String(150), nullable=True)
    reason        = sql.Column(sql.String(150), nullable=True)
    replaces      = sql.Column(sql.String(150), nullable=True)
    repository    = sql.Column(sql.String(150), nullable=True)
    required_by   = sql.Column(sql.String(150), nullable=True)
        

class Packages(sql.Model, PackageTemplate):
    pass    


class Apps(sql.Model, PackageTemplate, ScreenshotsTemplate):
    pass
    

class Snaps(sql.Model, BaseTemplate, ScreenshotsTemplate):
    channel    = sql.Column(sql.String(150), nullable=True)
    channels   = sql.Column(sql.String(150), nullable=True)
    confined   = sql.Column(sql.String(150), nullable=True)
    publisher  = sql.Column(sql.String(150), nullable=True)
    repository = sql.Column(sql.String(150), nullable=True)
    

class Flatpaks(sql.Model, BaseTemplate, ScreenshotsTemplate):
    pass


class Discover(sql.Model):
    id           = sql.Column(sql.Integer, primary_key=True)
    last_updated = sql.Column(sql.String(100), nullable=True)
    
