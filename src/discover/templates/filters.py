import json

def truncate_description(long_description: str, characters: int = 80):
    """ 
    desc: truncate long description strings to 80 char 
    usage: {{ description | truncate_description(characters=20)
    """
    if long_description:
        if len(long_description) <= characters:
            return long_description
        small_description = long_description[:characters].split(" ")[:-1]
        return " ".join(small_description)+'…'



def remove_pkg_symbols(dependecy):
    if ">" in dependecy:
        return dependecy.split(">")[0]
    elif "=" in dependecy:
        return dependecy.split("=")[0]
    else:
        return dependecy


def split_version(pkg):
    if ">=" in pkg:
        return pkg.split(">=")
    elif ">" in pkg:
        return pkg.split(">")
    elif "=" in pkg:
        return pkg.split("=")
    else:
        return [pkg]
