import subprocess
from discover.database import Database
from Manjaro.SDK import Utils

@Utils._async
def update_system():
    subprocess.run(
       "pacman-mirrors -f 5 && pacman -Syy --noconfirm archlinux-appstream-data", shell=True
      )
    Database().reload_tables()
