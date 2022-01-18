import subprocess
from discover.database import Database


def update_system():
    subprocess.run(
       "pacman-mirrors -f 5 && pacman -Syy --noconfirm archlinux-appstream-data", shell=True
      )
    Database().reload_tables()
