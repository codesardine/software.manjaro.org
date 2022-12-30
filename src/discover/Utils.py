import subprocess
from discover.database import Database
from Manjaro.SDK import Utils
from discover import app

@Utils._async
def update_system():
    subprocess.run(
       "pacman -Syy --noconfirm archlinux-appstream-data", shell=True
      )
    with app.app_context():
      Database().reload_tables()
