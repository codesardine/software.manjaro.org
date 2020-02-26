from flask import Flask

#@app.template_filter('trunc_desc')
def truncate_desc(desc: str, maxi: int = 160):
    """ troncate long text to word"""
    if len(desc) <= maxi:
        return desc
    desc = desc[:maxi]
    sdesc = desc.split(" ")[:-1]
    return " ".join(sdesc)+'…'

#@app.template_filter('class_manjaro')
def get_class_manjaro(pkg):
    """manjaro-app:project manjaro - manjaro-pkg:package by manjaro"""
    manja = ""
    if "manjaro.org" in pkg.get_packager():
        manja = "pkg"
    if "manjaro.org" in pkg.get_url():
        manja = "app"
    if manja < 1:
        return ""
    return f"manjaro-{manja}"
