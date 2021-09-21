import subprocess
from discover.database import Database

def truncate_description(long_description: str, characters: int = 160):
    """ 
    desc: truncate long description strings to 160 char 
    usage: {{ description | truncate_description(characters=20)
    """
    if long_description:
        if len(long_description) <= characters:
            return long_description
        small_description = long_description[:characters].split(" ")[:-1]
        return " ".join(small_description)+'…'


def update_system():
    subprocess.run(
        "pacman-mirrors --fasttrack && pacman -Syy --noconfirm archlinux-appstream-data", shell=True
        )
    Database().reload_tables()
